from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from endobella.auth import views


router = DefaultRouter()
router.register("users", views.UserViewSet, basename="user")


urlpatterns = [
    path("jwt/create/", views.TokenObtainPairView.as_view(), name="auth-jwt-create"),
    path(
        "jwt/email-login/",
        views.UserEmailLoginView.as_view(),
        name="auth-jwt-email-login",
    ),
    path(
        "jwt/create-by-token/",
        views.UserEmailLoginTokenObtainView.as_view(),
        name="auth-jwt-create-by-token",
    ),
    path("", include("djoser.urls.jwt")),
    *router.urls,
]
