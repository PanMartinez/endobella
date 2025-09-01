from __future__ import annotations

from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    name = "endobella.auth"
    label = "user_auth"
    verbose_name = "Authentication"
