from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.FileUploadView.as_view(), name='file_upload'),
    path('history/', views.upload_history, name='upload_history'),
    path('status/<int:upload_id>/', views.upload_status, name='upload_status'),
    path('delete/<int:upload_id>/', views.delete_upload_data, name='delete_upload_data'),
    path('delete-all/', views.delete_all_data, name='delete_all_data'),
]

