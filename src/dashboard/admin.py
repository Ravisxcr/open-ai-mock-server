from django.contrib import admin
from .models import StoredFile
from .models import VectorStore, VectorEntry


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "uploaded_at")
    search_fields = ("name", "user__username")


@admin.register(VectorStore)
class VectorStoreAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user__username")


@admin.register(VectorEntry)
class VectorEntryAdmin(admin.ModelAdmin):
    list_display = ("document_name", "vector_store", "created_at")
    search_fields = ("document_name", "vector_store__name")
