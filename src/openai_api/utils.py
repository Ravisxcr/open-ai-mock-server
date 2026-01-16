import uuid
import time
import random


def generate_request_id():
    """Generate a request ID similar to OpenAI's format"""
    return f"req_{uuid.uuid4().hex[:24]}"


def generate_chat_completion_response(messages, model="gpt-3.5-turbo", max_tokens=150):
    """Generate a mock chat completion response"""

    # Mock responses based on common patterns
    mock_responses = [
        "Hello! I'm a mock OpenAI assistant. How can I help you today?",
        "I understand you're looking for assistance. While I'm a simulation, I'll do my best to provide helpful responses.",
        "That's an interesting question! As a mock AI, I can provide sample responses for testing purposes.",
        "I'm here to help! Please note that this is a mock OpenAI server for development and testing.",
        "Thank you for your message. This is a simulated response from our mock OpenAI API server.",
    ]

    # Calculate tokens (rough approximation)
    prompt_tokens = sum(len(msg.get("content", "").split()) for msg in messages)
    completion_tokens = random.randint(10, max_tokens // 10)
    total_tokens = prompt_tokens + completion_tokens

    # Choose a random response or generate based on last message
    last_message = messages[-1].get("content", "") if messages else ""
    if "hello" in last_message.lower() or "hi" in last_message.lower():
        response_content = "Hello! How can I assist you today?"
    elif "test" in last_message.lower():
        response_content = "This is a test response from the mock OpenAI server."
    else:
        response_content = random.choice(mock_responses)

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:29]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": response_content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
        },
    }


def generate_embedding_response(input_text, model="text-embedding-ada-002"):
    """Generate a mock embedding response"""

    # Generate mock embedding (random vector)
    embedding_size = 1536  # OpenAI's ada-002 embedding size
    embedding = [random.uniform(-1, 1) for _ in range(embedding_size)]

    # Calculate tokens
    tokens = (
        len(input_text.split())
        if isinstance(input_text, str)
        else sum(len(text.split()) for text in input_text)
    )

    return {
        "object": "list",
        "data": [{"object": "embedding", "index": 0, "embedding": embedding}],
        "model": model,
        "usage": {"prompt_tokens": tokens, "total_tokens": tokens},
    }


def generate_moderation_response(input_text):
    """Generate a mock moderation response"""

    # Simple mock moderation logic
    flagged_words = ["hate", "violence", "self-harm", "sexual", "harassment"]
    text_lower = (
        input_text.lower()
        if isinstance(input_text, str)
        else " ".join(input_text).lower()
    )

    categories = {
        "hate": any(
            word in text_lower for word in ["hate", "racist", "discrimination"]
        ),
        "hate/threatening": False,
        "harassment": "harassment" in text_lower,
        "harassment/threatening": False,
        "self-harm": "self-harm" in text_lower or "suicide" in text_lower,
        "self-harm/intent": False,
        "self-harm/instructions": False,
        "sexual": "sexual" in text_lower or "porn" in text_lower,
        "sexual/minors": False,
        "violence": "violence" in text_lower or "kill" in text_lower,
        "violence/graphic": False,
    }

    category_scores = {
        key: random.uniform(0, 0.1) if not flagged else random.uniform(0.7, 0.9)
        for key, flagged in categories.items()
    }

    return {
        "id": f"modr-{uuid.uuid4().hex[:24]}",
        "model": "text-moderation-latest",
        "results": [
            {
                "flagged": any(categories.values()),
                "categories": categories,
                "category_scores": category_scores,
            }
        ],
    }


def generate_image_response(prompt, n=1, size="1024x1024"):
    """Generate a mock image generation response"""

    # Generate mock image URLs (placeholder service)
    images = []
    for i in range(n):
        images.append(
            {
                "url": f"https://picsum.photos/{size.replace('x', '/')}?random={uuid.uuid4().hex[:8]}"
            }
        )

    return {"created": int(time.time()), "data": images}


def get_available_models():
    """Return list of available models"""
    models = [
        {"id": "gpt-4", "object": "model", "created": 1687882411, "owned_by": "openai"},
        {
            "id": "gpt-4-turbo-preview",
            "object": "model",
            "created": 1706037777,
            "owned_by": "openai",
        },
        {
            "id": "gpt-3.5-turbo",
            "object": "model",
            "created": 1677610602,
            "owned_by": "openai",
        },
        {
            "id": "text-embedding-ada-002",
            "object": "model",
            "created": 1671217299,
            "owned_by": "openai",
        },
        {
            "id": "dall-e-3",
            "object": "model",
            "created": 1698785189,
            "owned_by": "openai",
        },
        {
            "id": "text-moderation-latest",
            "object": "model",
            "created": 1680870498,
            "owned_by": "openai",
        },
    ]

    return {"object": "list", "data": models}
