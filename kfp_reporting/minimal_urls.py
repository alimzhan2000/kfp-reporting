# Минимальные URL для тестирования Railway
from django.urls import path
from django.http import HttpResponse

def simple_response(request):
    """Максимально простой ответ"""
    return HttpResponse("Railway Django App is working!", content_type="text/plain")

urlpatterns = [
    path('', simple_response, name='home'),
    path('test/', simple_response, name='test'),
    path('health/', simple_response, name='health'),
]
