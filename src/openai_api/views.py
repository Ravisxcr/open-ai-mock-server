from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api_keys.models import APIKeyUsage
from api_keys.authentication import APIKeyAuthentication
from .utils import (
    generate_chat_completion_response,
    generate_embedding_response,
    generate_moderation_response,
    generate_image_response,
    get_available_models,
    generate_request_id,
)
import time


class BaseOpenAIView(APIView):
    """Base view for OpenAI API endpoints"""

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def log_usage(
        self,
        request,
        endpoint,
        model,
        tokens_input=0,
        tokens_output=0,
        status_code=200,
        error_message="",
        response_time_ms=0,
    ):
        """Log API usage for tracking"""
        try:
            api_key = request.auth
            if api_key:
                APIKeyUsage.objects.create(
                    api_key=api_key,
                    endpoint=endpoint,
                    model=model,
                    tokens_input=tokens_input,
                    tokens_output=tokens_output,
                    total_tokens=tokens_input + tokens_output,
                    user_agent=request.META.get("HTTP_USER_AGENT", ""),
                    ip_address=self.get_client_ip(request),
                    request_id=generate_request_id(),
                    response_time_ms=response_time_ms,
                    status_code=status_code,
                    error_message=error_message,
                )

                # Update API key total usage
                api_key.total_requests += 1
                api_key.total_tokens += tokens_input + tokens_output
                api_key.save(update_fields=["total_requests", "total_tokens"])
        except Exception as e:
            # Don't let logging errors break the API
            print(f"Error logging usage: {e}")

    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def validate_permissions(self, permission_field):
        """Check if API key has required permissions"""
        api_key = self.request.auth
        if not getattr(api_key, permission_field, True):
            return False
        return True


class ChatCompletionsView(BaseOpenAIView):
    """OpenAI Chat Completions API endpoint"""

    def post(self, request):
        start_time = time.time()

        try:
            # Check permissions
            if not self.validate_permissions("can_chat_completions"):
                return Response(
                    {
                        "error": {
                            "message": "API key does not have permission for chat completions"
                        }
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data
            messages = data.get("messages", [])
            model = data.get("model", "gpt-3.5-turbo")
            max_tokens = data.get("max_tokens", 150)

            if not messages:
                return Response(
                    {"error": {"message": "Messages are required"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate response
            response_data = generate_chat_completion_response(
                messages, model, max_tokens
            )

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Log usage
            usage = response_data.get("usage", {})
            self.log_usage(
                request=request,
                endpoint="chat_completions",
                model=model,
                tokens_input=usage.get("prompt_tokens", 0),
                tokens_output=usage.get("completion_tokens", 0),
                status_code=200,
                response_time_ms=response_time_ms,
            )

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self.log_usage(
                request=request,
                endpoint="chat_completions",
                model=data.get("model", "gpt-3.5-turbo"),
                status_code=500,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )

            return Response(
                {"error": {"message": "Internal server error"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EmbeddingsView(BaseOpenAIView):
    """OpenAI Embeddings API endpoint"""

    def post(self, request):
        start_time = time.time()

        try:
            # Check permissions
            if not self.validate_permissions("can_embeddings"):
                return Response(
                    {
                        "error": {
                            "message": "API key does not have permission for embeddings"
                        }
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data
            input_text = data.get("input", "")
            model = data.get("model", "text-embedding-ada-002")

            if not input_text:
                return Response(
                    {"error": {"message": "Input is required"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate response
            response_data = generate_embedding_response(input_text, model)

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Log usage
            usage = response_data.get("usage", {})
            self.log_usage(
                request=request,
                endpoint="embeddings",
                model=model,
                tokens_input=usage.get("prompt_tokens", 0),
                tokens_output=0,
                status_code=200,
                response_time_ms=response_time_ms,
            )

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self.log_usage(
                request=request,
                endpoint="embeddings",
                model=data.get("model", "text-embedding-ada-002"),
                status_code=500,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )

            return Response(
                {"error": {"message": "Internal server error"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ModerationsView(BaseOpenAIView):
    """OpenAI Moderations API endpoint"""

    def post(self, request):
        start_time = time.time()

        try:
            # Check permissions
            if not self.validate_permissions("can_moderations"):
                return Response(
                    {
                        "error": {
                            "message": "API key does not have permission for moderations"
                        }
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data
            input_text = data.get("input", "")

            if not input_text:
                return Response(
                    {"error": {"message": "Input is required"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate response
            response_data = generate_moderation_response(input_text)

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Log usage
            self.log_usage(
                request=request,
                endpoint="moderations",
                model="text-moderation-latest",
                tokens_input=len(input_text.split())
                if isinstance(input_text, str)
                else 0,
                tokens_output=0,
                status_code=200,
                response_time_ms=response_time_ms,
            )

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self.log_usage(
                request=request,
                endpoint="moderations",
                model="text-moderation-latest",
                status_code=500,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )

            return Response(
                {"error": {"message": "Internal server error"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ImagesGenerationsView(BaseOpenAIView):
    """OpenAI Images Generations API endpoint"""

    def post(self, request):
        start_time = time.time()

        try:
            # Check permissions
            if not self.validate_permissions("can_images"):
                return Response(
                    {
                        "error": {
                            "message": "API key does not have permission for image generation"
                        }
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data
            prompt = data.get("prompt", "")
            n = data.get("n", 1)
            size = data.get("size", "1024x1024")

            if not prompt:
                return Response(
                    {"error": {"message": "Prompt is required"}},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate response
            response_data = generate_image_response(prompt, n, size)

            # Calculate response time
            response_time_ms = int((time.time() - start_time) * 1000)

            # Log usage
            self.log_usage(
                request=request,
                endpoint="images_generations",
                model="dall-e-3",
                tokens_input=len(prompt.split()),
                tokens_output=0,
                status_code=200,
                response_time_ms=response_time_ms,
            )

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            self.log_usage(
                request=request,
                endpoint="images_generations",
                model="dall-e-3",
                status_code=500,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )

            return Response(
                {"error": {"message": "Internal server error"}},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ModelsView(APIView):
    """OpenAI Models API endpoint"""

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List available models"""
        return Response(get_available_models(), status=status.HTTP_200_OK)


class ModelDetailsView(APIView):
    """OpenAI Model Details API endpoint"""

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, model_id):
        """Get details for a specific model"""
        models_data = get_available_models()

        for model in models_data["data"]:
            if model["id"] == model_id:
                return Response(model, status=status.HTTP_200_OK)

        return Response(
            {"error": {"message": f"Model {model_id} not found"}},
            status=status.HTTP_404_NOT_FOUND,
        )
