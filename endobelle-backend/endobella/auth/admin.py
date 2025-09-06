from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "first_name",
        "last_name",
    )
    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
    )

    search_fields = ("email", "id")
    ordering = ("email",)
