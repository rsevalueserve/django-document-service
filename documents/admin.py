from django.contrib import admin
from .models import Document
import mimetypes

class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('size', 'content_type', 'uploaded_at')
    def save_model(self, request, obj, form, change):
        if obj.file:
            obj.size = obj.file.size
            # Try to get content_type from file object, fallback to mimetypes
            ct = getattr(obj.file, 'content_type', None)
            if not ct:
                ct, _ = mimetypes.guess_type(obj.file.name)
            obj.content_type = ct or ''
        super().save_model(request, obj, form, change)

admin.site.register(Document, DocumentAdmin)

# Register your models here.
