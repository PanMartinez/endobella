from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import (
    SendEmailResetSerializer,
    UidAndTokenSerializer,
    UserCreateSerializer as DjoserUserCreateSerializer,
)
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer,
)
from rest_framework_simplejwt.settings import api_settings

from endobella.auth.models import User


USER_FIELDS = ["id", "email", "first_name", "last_name", "dt_created", "dt_updated"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        ref_name = "AuthUser"
        fields = USER_FIELDS


class LowercaseEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return value.lower()

    def to_representation(self, value):
        representation = super().to_representation(value)
        return representation.lower()


class UserCreateSerializer(DjoserUserCreateSerializer):
    email = LowercaseEmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email address already exists.",
            )
        ]
    )
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        ref_name = "AuthUserCreate"
        fields = [
            *USER_FIELDS,
            "token",
        ]


class ActivateSerializer(UidAndTokenSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True, required=True
    )

    def validate(self, attrs) -> dict:
        user: User | None = self.context.get("user")
        try:
            validate_password(attrs["password"], user)
        except django_exceptions.ValidationError as e:
            raise ValidationError({"password": list(e.messages)}) from e

        return attrs


class ResendActivationSerializer(SendEmailResetSerializer):
    pass


class UserEmailLoginSerializer(serializers.Serializer):
    email = LowercaseEmailField()
    redirect_url = serializers.CharField(allow_blank=True, required=False)


class EmailLoginTokenObtainSerializer(TokenObtainPairSerializer, UidAndTokenSerializer):
    def __init__(self, *args, **kwargs):
        super(TokenObtainSerializer, self).__init__(*args, **kwargs)

    def validate(self, attrs):
        super(TokenObtainSerializer, self).validate(attrs)
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
