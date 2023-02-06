from django.urls import path

from dl import views

urlpatterns = [
    path('', views.FileUploadView.as_view(), name='upload'),
    path('<int:pk>/', views.FileDownloadView.as_view(), name='download'),
    path('list/', views.FileListView.as_view(), name='list'),
]
