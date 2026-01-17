from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import TemplateView, CreateView, DeleteView, View
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from api_keys.models import APIKey, APIKeyUsage
from .forms import CustomUserCreationForm, APIKeyForm
from .models import StoredFile
from django.views.generic.edit import FormView
from django import forms
from django.views.generic import ListView, DetailView
from .models import VectorStore, VectorEntry
from .forms import VectorStoreForm, VectorEntryForm
from django.http import FileResponse


class RegisterView(CreateView):
    """User registration view"""

    form_class = CustomUserCreationForm
    template_name = "dashboard/register.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Account created successfully!")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard view"""

    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user's API keys
        api_keys = APIKey.objects.filter(user=user)
        context["total_api_keys"] = api_keys.count()
        context["active_api_keys"] = api_keys.filter(status="active").count()

        # Get usage statistics
        now = timezone.now()
        today = now.date()
        last_30_days = now - timedelta(days=30)

        usage_stats = APIKeyUsage.objects.filter(
            api_key__user=user, created_at__gte=last_30_days
        ).aggregate(
            total_requests=Count("id"),
            total_tokens=Sum("total_tokens"),
            today_requests=Count("id", filter=Q(created_at__date=today)),
        )

        context.update(
            {
                "total_requests": usage_stats.get("total_requests", 0),
                "total_tokens": usage_stats.get("total_tokens", 0),
                "today_requests": usage_stats.get("today_requests", 0),
                "recent_api_keys": api_keys.order_by("-created_at")[:5],
            }
        )

        return context


class APIKeysView(LoginRequiredMixin, TemplateView):
    """API keys management view"""

    template_name = "dashboard/api_keys.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["api_keys"] = APIKey.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )
        return context


class CreateAPIKeyView(LoginRequiredMixin, CreateView):
    """Create new API key"""

    model = APIKey
    form_class = APIKeyForm
    template_name = "dashboard/create_api_key.html"
    success_url = reverse_lazy("api_keys")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request, f'API key "{form.instance.name}" created successfully!'
        )
        return response


class DeleteAPIKeyView(LoginRequiredMixin, DeleteView):
    """Delete API key"""

    model = APIKey
    template_name = "dashboard/delete_api_key.html"
    success_url = reverse_lazy("api_keys")

    def get_queryset(self):
        return APIKey.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        api_key = self.get_object()
        name = api_key.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'API key "{name}" deleted successfully!')
        return response


class ToggleAPIKeyView(LoginRequiredMixin, View):
    """Toggle API key status"""

    def post(self, request, pk):
        api_key = get_object_or_404(APIKey, pk=pk, user=request.user)

        if api_key.status == "active":
            api_key.status = "suspended"
            action = "suspended"
        else:
            api_key.status = "active"
            action = "activated"

        api_key.save()
        messages.success(request, f'API key "{api_key.name}" {action} successfully!')

        return redirect("api_keys")


class UsageView(LoginRequiredMixin, TemplateView):
    """Usage analytics view"""

    template_name = "dashboard/usage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get date range (last 30 days by default)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)

        # Get usage data
        usage_data = APIKeyUsage.objects.filter(
            api_key__user=user, created_at__gte=start_date
        )

        # Group by date
        daily_usage = {}
        for usage in usage_data:
            date = usage.created_at.date()
            if date not in daily_usage:
                daily_usage[date] = {"requests": 0, "tokens": 0}
            daily_usage[date]["requests"] += 1
            daily_usage[date]["tokens"] += usage.total_tokens

        # Group by endpoint
        endpoint_usage = usage_data.values("endpoint").annotate(
            requests=Count("id"), tokens=Sum("total_tokens")
        )

        # Group by API key
        api_key_usage = usage_data.values("api_key__name").annotate(
            requests=Count("id"), tokens=Sum("total_tokens")
        )

        context.update(
            {
                "daily_usage": daily_usage,
                "endpoint_usage": endpoint_usage,
                "api_key_usage": api_key_usage,
                "total_usage": usage_data.count(),
                "date_range": f"{start_date.date()} to {end_date.date()}",
            }
        )

        return context


class APIKeyUsageView(LoginRequiredMixin, TemplateView):
    """Specific API key usage view"""

    template_name = "dashboard/usage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_key = get_object_or_404(APIKey, pk=kwargs["pk"], user=self.request.user)

        # Get date range (last 30 days by default)
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)

        # Get usage data for this specific API key
        usage_data = APIKeyUsage.objects.filter(
            api_key=api_key, created_at__gte=start_date
        )

        # Group by date
        daily_usage = {}
        for usage in usage_data:
            date = usage.created_at.date()
            if date not in daily_usage:
                daily_usage[date] = {"requests": 0, "tokens": 0}
            daily_usage[date]["requests"] += 1
            daily_usage[date]["tokens"] += usage.total_tokens or 0

        # Group by endpoint
        endpoint_usage = (
            usage_data.values("endpoint")
            .annotate(requests=Count("id"), tokens=Sum("total_tokens"))
            .order_by("-requests")
        )

        # For single API key view, we just show this one key's usage
        api_key_usage = [
            {
                "api_key__name": api_key.name,
                "requests": usage_data.count(),
                "tokens": usage_data.aggregate(total_tokens=Sum("total_tokens"))[
                    "total_tokens"
                ]
                or 0,
            }
        ]

        context.update(
            {
                "daily_usage": daily_usage,
                "endpoint_usage": endpoint_usage,
                "api_key_usage": api_key_usage,
                "total_usage": usage_data.count(),
                "date_range": f"{start_date.date()} to {end_date.date()}",
                "api_key": api_key,  # Add the specific API key for context
            }
        )

        return context


class SettingsView(LoginRequiredMixin, TemplateView):
    """User settings view"""

    template_name = "dashboard/settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get user's API keys
        api_keys = APIKey.objects.filter(user=user)

        # Calculate statistics
        total_requests = sum(key.total_requests for key in api_keys)
        total_tokens = sum(key.total_tokens for key in api_keys)
        active_keys_count = api_keys.filter(status="active").count()

        context.update(
            {
                "user": user,
                "total_api_keys": api_keys.count(),
                "active_keys_count": active_keys_count,
                "total_requests": total_requests,
                "total_tokens": total_tokens,
            }
        )

        return context


class DocumentationView(LoginRequiredMixin, TemplateView):
    """API Documentation view"""

    template_name = "dashboard/documentation.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StoredFileUploadForm(forms.ModelForm):
    class Meta:
        model = StoredFile
        fields = ["file", "name"]


class FileListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/files.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["files"] = StoredFile.objects.filter(user=self.request.user).order_by(
            "-uploaded_at"
        )
        return context


class FileUploadView(LoginRequiredMixin, FormView):
    form_class = StoredFileUploadForm
    template_name = "dashboard/upload_file.html"
    success_url = reverse_lazy("file_list")

    def form_valid(self, form):
        stored_file = form.save(commit=False)
        stored_file.user = self.request.user
        stored_file.save()
        messages.success(
            self.request, f'File "{stored_file.name}" uploaded successfully!'
        )
        return super().form_valid(form)


class FileDeleteView(LoginRequiredMixin, DeleteView):
    model = StoredFile
    template_name = "dashboard/delete_file.html"
    success_url = reverse_lazy("file_list")

    def get_queryset(self):
        return StoredFile.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        file_obj = self.get_object()
        name = file_obj.name
        if file_obj.file:
            file_obj.file.delete(save=False)
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'File "{name}" deleted successfully!')
        return response
    

class FileDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        stored_file = get_object_or_404(
            StoredFile,
            pk=pk,
            user=request.user,
        )

        return FileResponse(
            stored_file.file.open("rb"),
            as_attachment=True,
            filename=stored_file.name,
        )


class VectorStoreListView(LoginRequiredMixin, ListView):
    model = VectorStore
    template_name = "dashboard/vector_stores.html"
    context_object_name = "vector_stores"

    def get_queryset(self):
        return VectorStore.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )


class VectorStoreCreateView(LoginRequiredMixin, CreateView):
    model = VectorStore
    form_class = VectorStoreForm
    template_name = "dashboard/create_vector_store.html"
    success_url = reverse_lazy("vector_store_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, f'Vector Store "{form.instance.name}" created!')
        return super().form_valid(form)


class VectorStoreDetailView(LoginRequiredMixin, DetailView):
    model = VectorStore
    template_name = "dashboard/vector_store_detail.html"
    context_object_name = "vector_store"

    def get_queryset(self):
        return VectorStore.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = self.object.entries.all().order_by("-created_at")
        return context


class VectorEntryCreateView(LoginRequiredMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["store_pk"] = self.kwargs["store_pk"]
        return context

    model = VectorEntry
    form_class = VectorEntryForm
    template_name = "dashboard/create_vector_entry.html"

    def get_success_url(self):
        return reverse_lazy(
            "vector_store_detail", kwargs={"pk": self.object.vector_store.pk}
        )

    def form_valid(self, form):
        from .models import VectorStore

        store_pk = self.kwargs["store_pk"]
        form.instance.vector_store = VectorStore.objects.get(
            pk=store_pk, user=self.request.user
        )
        messages.success(self.request, f'Entry "{form.instance.document_name}" added!')
        return super().form_valid(form)
