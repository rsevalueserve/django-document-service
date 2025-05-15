from django.urls import path
from .views import DocumentList, DocumentDetail, DocumentDownload

urlpatterns = [
    path('documents/', DocumentList.as_view(), name='document-list'),
    path('documents/<int:pk>/', DocumentDetail.as_view(), name='document-detail'),
    path('documents/<int:pk>/download/', DocumentDownload.as_view(), name='document-download'),
]
