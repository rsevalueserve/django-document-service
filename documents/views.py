from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404
from .models import Document
from .serializers import DocumentSerializer
import os
import mimetypes

class DocumentList(APIView):
    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
        content_type = file.content_type or mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
        document = Document(
            file=file,
            name=file.name,
            size=file.size,
            content_type=content_type
        )
        document.save()
        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DocumentDetail(APIView):
    def get_object(self, pk):
        return get_object_or_404(Document, pk=pk)

    def get(self, request, pk):
        document = self.get_object(pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            document = self.get_object(pk)
        except Http404:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if document.file:
            document.file.delete(save=False)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DocumentDownload(APIView):
    def get(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        if hasattr(document.file, 'url'):
            return Response({'url': document.file.url})
        file_path = document.file.path
        if not os.path.exists(file_path):
            raise Http404
        response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=document.name)
        return response
