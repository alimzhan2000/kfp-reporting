"""
URL маршруты для управления пользователями
"""
from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.list_users, name='list_users'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/', views.get_user, name='get_user'),
    path('users/<int:user_id>/update/', views.update_user, name='update_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/initialize-demo/', views.initialize_demo_users, name='initialize_demo_users'),
    path('users/force-initialize/', views.force_initialize_database, name='force_initialize_database'),
    path('users/database-status/', views.check_database_status, name='check_database_status'),
]