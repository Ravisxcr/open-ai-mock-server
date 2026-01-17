from django.db import models
from django.conf import settings


class StoredFile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="files"
    )
    file = models.FileField(upload_to="user_files/")
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VectorStore(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vector_stores"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class VectorEntry(models.Model):
    vector_store = models.ForeignKey(
        VectorStore, on_delete=models.CASCADE, related_name="entries"
    )
    document_name = models.CharField(max_length=255)
    embedding = models.JSONField()  # Store as list of floats (vector)
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} in {self.vector_store.name}"
