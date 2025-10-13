"""
Admin configuration for accounts app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'

class ExtendedUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'get_is_active_user', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'date_joined', 'profile__role', 'profile__is_active_user')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__phone', 'profile__department')
    ordering = ('-date_joined',)
    
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except:
            return 'Пользователь'
    get_role.short_description = 'Роль'
    
    def get_is_active_user(self, obj):
        try:
            return obj.profile.is_active_user
        except:
            return True
    get_is_active_user.short_description = 'Активный пользователь'
    get_is_active_user.boolean = True

# Отменяем регистрацию стандартной модели User и регистрируем расширенную
admin.site.unregister(User)
admin.site.register(User, ExtendedUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'department', 'is_active_user', 'created_at')
    list_filter = ('role', 'is_active_user', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone', 'department')
    ordering = ('-created_at',)