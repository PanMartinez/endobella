from __future__ import annotations

from django.contrib.auth.tokens import default_token_generator
from djoser.serializers import UidAndTokenSerializer
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


from endobella.auth.models import User
from endobella.auth.serializers import (
    ActivateSerializer,
    EmailLoginTokenObtainSerializer,
    ResendActivationSerializer,
    UserCreateSerializer,
    UserEmailLoginSerializer,
    UserSerializer,
)


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    lookup_field = "hid"
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(pk=user.pk)

    def get_serializer_class(self):
        if self.action == "me":
            return UserSerializer
        if self.action == "create":
            return UserCreateSerializer
        return super().get_serializer_class()

    @action(["get", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        if request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        return None

    @action(
        ["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        url_path="activation",
    )
    def activation(self, request, *args, **kwargs):
        data = request.data
        serializer = UidAndTokenSerializer(data=data, context={"view": self})
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        if user.is_active:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"user": "This account is already active"},
            )
        user_serializer = UserSerializer(user)

        if user.password:
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={"password": "Password already created for this user"},
            )

        serializer = ActivateSerializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        supplied_password = request.data.get("password")
        user.set_password(supplied_password)
        user.is_active = True
        user.save()
        token_serializer = TokenObtainPairSerializer(
            data={"email": user.email, "password": supplied_password}
        )
        token_serializer.is_valid(raise_exception=True)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "user": user_serializer.data,
                "token": token_serializer.validated_data,
            },
        )

    @action(
        ["post"],
        detail=False,
        permission_classes=[permissions.AllowAny],
        url_path="validate-activation-link",
    )
    def validate_activation_link(self, request, *args, **kwargs):
        data = request.data
        serializer = UidAndTokenSerializer(data=data, context={"view": self})
        serializer.is_valid(raise_exception=True)
        if serializer.user.is_active:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"user": "This account is already active"},
            )
        user_serializer = UserSerializer(serializer.user)
        return Response(data=user_serializer.data)

    @action(["post"], detail=False, url_path="resend-activation")
    def resend_activation(self, request, *args, **kwargs):
        serializer = ResendActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)
        if not user:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={
                    "email": "Email is not associated with any user or user is active"
                },
            )

        # TODO send email here
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path="set-password")
    def set_password(self, request, *args, **kwargs):
        return super().set_password(request, *args, **kwargs)

    @action(["post"], detail=False, url_path=f"reset-{User.USERNAME_FIELD}")
    def reset_username(self, request, *args, **kwargs):
        return super().reset_username(request, *args, **kwargs)

    @action(["post"], detail=False, url_path=f"reset-{User.USERNAME_FIELD}-confirm")
    def reset_username_confirm(self, request, *args, **kwargs):
        return super().reset_username_confirm(request, *args, **kwargs)

    @action(["post"], detail=False, url_path="reset-password-confirm")
    def reset_password_confirm(self, request, *args, **kwargs):
        return super().reset_password_confirm(request, *args, **kwargs)

    @action(["post"], detail=False, url_path="reset-password")
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            # TODO send email here
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=False, url_path=f"set-{User.USERNAME_FIELD}")
    def set_username(self, request, *args, **kwargs):
        return super().set_username(request, *args, **kwargs)


class UserEmailLoginView(generics.GenericAPIView):
    serializer_class = UserEmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        redirect_url = serializer.validated_data.get("redirect_url")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise NotFound() from e

        context = {"user": user, "redirect_url": redirect_url}
        # TODO send email here

        return Response(context, status=status.HTTP_204_NO_CONTENT)


class UserEmailLoginTokenObtainView(TokenObtainPairView):
    serializer_class = EmailLoginTokenObtainSerializer
    token_generator = default_token_generator

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        user_serializer = UserSerializer(serializer.user)
        response_data = {
            "user": user_serializer.data,
            "token": serializer.validated_data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
