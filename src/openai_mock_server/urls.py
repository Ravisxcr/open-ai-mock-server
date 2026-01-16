"""
URL configuration for openai_mock_server project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("v1/", include("openai_api.urls")),
    path("", include("dashboard.urls")),  # Default to dashboard
]
