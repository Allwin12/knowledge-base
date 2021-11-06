from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryView.as_view(), name='category'),
    path('upload/', views.DocumentUploadView.as_view(), name='document-upload'),
    path('document-search/', views.DocumentView.as_view(), name='document-search'),
    path('knowledge-base/', views.KnowledgeBaseView.as_view(), name='knowledge-base')
]
