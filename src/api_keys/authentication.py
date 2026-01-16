from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey
from datetime import datetime


class APIKeyUser:
    """Custom user class for API key authentication"""

    def __init__(self, api_key):
        self.api_key = api_key
        self.username = f"api_key_{api_key.id}"
        self.id = api_key.id
        self.is_authenticated = True
        self.is_anonymous = False

    def __str__(self):
        return self.username


class APIKeyAuthentication(BaseAuthentication):
    """
    Custom authentication class for API keys
    Expects Authorization header: Bearer sk-...
    """

    keyword = "Bearer"

    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if not auth_header:
            return None

        auth_parts = auth_header.split()

        if len(auth_parts) != 2 or auth_parts[0] != self.keyword:
            return None

        api_key_value = auth_parts[1]

        try:
            api_key = APIKey.objects.select_related("user").get(
                key=api_key_value, status="active"
            )
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API key")

        # Check if key is expired
        if not api_key.is_active:
            raise AuthenticationFailed("API key is expired or inactive")

        # Update last used timestamp
        api_key.last_used = datetime.now()
        api_key.save(update_fields=["last_used"])

        return (APIKeyUser(api_key), api_key)

    def authenticate_header(self, request):
        return self.keyword
