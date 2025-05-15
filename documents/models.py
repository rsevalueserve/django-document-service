from django.db import models
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class Document(models.Model):
    file = models.FileField(
        upload_to="documents/",
        storage=S3Boto3Storage() if getattr(settings, 'USE_S3', False) else None
    )
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()
    content_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name
