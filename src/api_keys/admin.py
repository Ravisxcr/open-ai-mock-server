from django.contrib import admin
from .models import APIKey, APIKeyUsage, RateLimitTracker


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "masked_key",
        "user",
        "plan",
        "status",
        "total_requests",
        "created_at",
    ]
    list_filter = ["plan", "status", "created_at"]
    search_fields = ["name", "user__username", "user__email"]
    readonly_fields = [
        "key",
        "id",
        "total_requests",
        "total_tokens",
        "last_used",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        ("Basic Information", {"fields": ("id", "name", "user", "key")}),
        ("Plan & Status", {"fields": ("plan", "status", "expires_at")}),
        ("Rate Limits", {"fields": ("requests_per_minute", "requests_per_day")}),
        (
            "Permissions",
            {
                "fields": (
                    "can_chat_completions",
                    "can_embeddings",
                    "can_moderations",
                    "can_images",
                )
            },
        ),
        (
            "Usage Statistics",
            {"fields": ("total_requests", "total_tokens", "last_used")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(APIKeyUsage)
class APIKeyUsageAdmin(admin.ModelAdmin):
    list_display = [
        "api_key",
        "endpoint",
        "model",
        "total_tokens",
        "status_code",
        "created_at",
    ]
    list_filter = ["endpoint", "model", "status_code", "created_at"]
    search_fields = ["api_key__name", "model", "request_id"]
    readonly_fields = ["id", "request_id", "created_at"]

    fieldsets = (
        (
            "Request Information",
            {"fields": ("id", "api_key", "endpoint", "model", "request_id")},
        ),
        ("Token Usage", {"fields": ("tokens_input", "tokens_output", "total_tokens")}),
        (
            "Response Details",
            {"fields": ("status_code", "response_time_ms", "error_message")},
        ),
        ("Metadata", {"fields": ("user_agent", "ip_address", "created_at")}),
    )


@admin.register(RateLimitTracker)
class RateLimitTrackerAdmin(admin.ModelAdmin):
    list_display = ["api_key", "window_type", "requests_count", "window_start"]
    list_filter = ["window_type", "window_start"]
    search_fields = ["api_key__name"]
