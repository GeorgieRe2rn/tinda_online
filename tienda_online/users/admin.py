from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'phone', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (('Datos de contacto', {'fields': ('phone',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Datos de contacto', {'fields': ('email', 'phone')}),)
