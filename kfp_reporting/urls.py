"""
URL configuration for kfp_reporting project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.simple_health, name='simple_health'),
    path('minimal/', views.minimal_health, name='minimal_health'),
    path('admin/', admin.site.urls),
    
    # Frontend pages
    path('upload/', views.upload_page, name='upload_page'),
    path('upload-test/', views.test_upload_page, name='test_upload_page'),
    path('simple-test/', views.simple_test_page, name='simple_test_page'),
    path('ultra-test/', views.ultra_simple_test_page, name='ultra_simple_test_page'),
    path('no-pandas-test/', views.no_pandas_test_page, name='no_pandas_test_page'),
    path('reports/', views.reports_page, name='reports_page'),
    path('reports/yield-comparison/', views.yield_comparison_report, name='yield_comparison_report'),
    path('data/', views.home, name='data_page'),  # Redirect to dashboard
    
    # API endpoints
    path('api/auth/', include('accounts.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/upload/', include('data_upload.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

