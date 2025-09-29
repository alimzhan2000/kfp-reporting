from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('create/', views.create_user, name='create_user'),
    path('list/', views.user_list, name='user_list'),
]

