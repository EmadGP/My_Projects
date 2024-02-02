from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Velden', {
            'fields': ('role',),
        }),
    )

admin.site.register(MyUser, CustomUserAdmin)
