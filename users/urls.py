from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    UserProfileViewSet,
    PaymentViewSet,
    UserCreateAPIView,
    SimplePaymentView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("users/me/", UserProfileViewSet.as_view({"get": "me"}), name="user-me"),
    path(
        "register/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("payments/", SimplePaymentView.as_view(), name="payments"),
] + router.urls
