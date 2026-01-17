from django.db import models
from django.contrib.auth.models import User
import uuid
import secrets
import string
from datetime import datetime
from core.models.base import UUIDTimeStampedModel


class APIKey(UUIDTimeStampedModel):
    """Model for managing API keys"""

    PLAN_CHOICES = [
        ("free", "Free"),
        ("basic", "Basic"),
        ("premium", "Premium"),
        ("enterprise", "Enterprise"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("suspended", "Suspended"),
        ("expired", "Expired"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=100, help_text="Friendly name for the API key")
    key = models.CharField(max_length=64, unique=True, db_index=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    # Rate limiting
    requests_per_minute = models.IntegerField(default=10)
    requests_per_day = models.IntegerField(default=1000)

    # Usage tracking
    total_requests = models.BigIntegerField(default=0)
    total_tokens = models.BigIntegerField(default=0)
    last_used = models.DateTimeField(null=True, blank=True)

    # Timestamps
    expires_at = models.DateTimeField(null=True, blank=True)

    # Permissions
    can_chat_completions = models.BooleanField(default=True)
    can_embeddings = models.BooleanField(default=True)
    can_moderations = models.BooleanField(default=True)
    can_images = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "API Key"
        verbose_name_plural = "API Keys"

    def __str__(self):
        return f"{self.name} ({self.key[:8]}...)"

    @classmethod
    def generate_key(cls):
        """Generate a new API key in OpenAI format: sk-..."""
        # Generate random string
        alphabet = string.ascii_letters + string.digits
        random_string = "".join(secrets.choice(alphabet) for _ in range(48))
        return f"sk-{random_string}"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """Check if API key is active and not expired"""
        if self.status != "active":
            return False
        if self.expires_at and self.expires_at < datetime.now().replace(tzinfo=None):
            return False
        return True

    @property
    def masked_key(self):
        """Return masked version of the key for display"""
        return f"{self.key[:8]}...{self.key[-4:]}"


class APIKeyUsage(models.Model):
    """Model for tracking API key usage"""

    ENDPOINT_CHOICES = [
        ("chat_completions", "Chat Completions"),
        ("embeddings", "Embeddings"),
        ("moderations", "Moderations"),
        ("images_generations", "Image Generations"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    api_key = models.ForeignKey(
        APIKey, on_delete=models.CASCADE, related_name="usage_records"
    )
    endpoint = models.CharField(max_length=50, choices=ENDPOINT_CHOICES)

    # Request details
    model = models.CharField(max_length=100)
    tokens_input = models.IntegerField(default=0)
    tokens_output = models.IntegerField(default=0)
    total_tokens = models.IntegerField(default=0)

    # Metadata
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    request_id = models.CharField(max_length=100, unique=True)

    # Response details
    response_time_ms = models.IntegerField(help_text="Response time in milliseconds")
    status_code = models.IntegerField()
    error_message = models.TextField(blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "API Key Usage"
        verbose_name_plural = "API Key Usage Records"

    def __str__(self):
        return f"{self.api_key.name} - {self.endpoint} - {self.created_at}"


class RateLimitTracker(models.Model):
    """Model for tracking rate limits"""

    api_key = models.ForeignKey(
        APIKey, on_delete=models.CASCADE, related_name="rate_limits"
    )
    window_start = models.DateTimeField()
    requests_count = models.IntegerField(default=0)
    window_type = models.CharField(
        max_length=10, choices=[("minute", "Minute"), ("day", "Day")]
    )

    class Meta:
        unique_together = ["api_key", "window_start", "window_type"]
        verbose_name = "Rate Limit Tracker"
        verbose_name_plural = "Rate Limit Trackers"
