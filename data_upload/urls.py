from django.urls import path
from . import views

urlpatterns = [
    path('file/', views.FileUploadView.as_view(), name='file_upload'),
    path('test/', views.TestFileProcessingView.as_view(), name='test_file_upload'),
    path('simple-test/', views.SimpleFileTestView.as_view(), name='simple_file_test'),
    path('ultra-test/', views.UltraSimpleTestView.as_view(), name='ultra_simple_test'),
    path('no-pandas-test/', views.NoPandasTestView.as_view(), name='no_pandas_test'),
    path('basic-python-test/', views.BasicPythonTestView.as_view(), name='basic_python_test'),
    path('history/', views.upload_history, name='upload_history'),
    path('status/<int:upload_id>/', views.upload_status, name='upload_status'),
    path('delete/<int:upload_id>/', views.delete_upload_data, name='delete_upload_data'),
    path('delete-all/', views.delete_all_data, name='delete_all_data'),
]

