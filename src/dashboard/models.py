from django.db import models
from django.conf import settings
from core.models.base import UUIDTimeStampedModel
import os
import uuid

def upload_to_uuid(instance, filename):
    """
    Rename file to UUID and keep original extension
    Example: user_files/<user_id>/<uuid>.pdf
    """
    ext = os.path.splitext(filename)[1]  # includes dot
    return f"files/{uuid.uuid4()}{ext}"


class StoredFile(UUIDTimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to=upload_to_uuid)
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and self.file:
            self.name = self.file.name
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.id)


class VectorStore(UUIDTimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vector_stores"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)


class VectorEntry(UUIDTimeStampedModel):
    vector_store = models.ForeignKey(
        VectorStore, on_delete=models.CASCADE, related_name="entries"
    )
    document_name = models.CharField(max_length=255)
    embedding = models.JSONField()  # Store as list of floats (vector)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.document_name} in {self.vector_store.name}"
