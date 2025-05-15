from django.urls import path
from .views import DocumentList, DocumentDetail, DocumentDownload

urlpatterns = [
    path('', DocumentList.as_view(), name='document-list'),
    path('<int:pk>/', DocumentDetail.as_view(), name='document-detail'),
    path('<int:pk>/download/', DocumentDownload.as_view(), name='document-download'),
]
