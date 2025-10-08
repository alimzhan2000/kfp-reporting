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
    path('api/auth/', include('accounts.urls')),
    path('api/reports/', include('reports.urls')),
    # path('api/upload/', include('data_upload.urls')),  # Временно отключено
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

