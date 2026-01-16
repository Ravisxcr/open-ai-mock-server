from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="dashboard/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    # Dashboard URLs
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("api-keys/", views.APIKeysView.as_view(), name="api_keys"),
    path("api-keys/create/", views.CreateAPIKeyView.as_view(), name="create_api_key"),
    path(
        "api-keys/<uuid:pk>/delete/",
        views.DeleteAPIKeyView.as_view(),
        name="delete_api_key",
    ),
    path(
        "api-keys/<uuid:pk>/toggle/",
        views.ToggleAPIKeyView.as_view(),
        name="toggle_api_key",
    ),
    # Usage and analytics
    path("usage/", views.UsageView.as_view(), name="usage"),
    path(
        "api-keys/<uuid:pk>/usage/",
        views.APIKeyUsageView.as_view(),
        name="api_key_usage",
    ),
    path("documentation/", views.DocumentationView.as_view(), name="documentation"),
    # Settings
    path("settings/", views.SettingsView.as_view(), name="settings"),
]
