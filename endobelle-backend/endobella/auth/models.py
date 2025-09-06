from typing import cast
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower
from django.utils.translation import gettext_lazy as _

from endobella.common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, email: str, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email is required."))
        email = self.normalize_email(email)
        user = cast(User, self.model(email=email, **extra_fields))
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    @classmethod
    def normalize_email(cls, email):
        email = email or ""
        return email.lower()


class User(BaseModel, AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"), blank=False, unique=True, db_index=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                name="user_email_case_insensitive_uniqueness",
            )
        ]

    def __str__(self):
        return self.email

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
