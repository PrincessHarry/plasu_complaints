from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_active']
    list_filter = ['role', 'is_active', 'department']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'matric_number', 'staff_id']
    ordering = ['username']

    fieldsets = UserAdmin.fieldsets + (
        ('PSU Profile', {
            'fields': ('role', 'matric_number', 'staff_id', 'department', 'phone_number', 'profile_picture')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PSU Profile', {
            'fields': ('role', 'matric_number', 'staff_id', 'department', 'phone_number')
        }),
    )
