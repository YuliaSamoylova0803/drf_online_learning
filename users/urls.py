from users.apps import UsersConfig
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet


app_name = UsersConfig.name


router = DefaultRouter()
router.register(r"", UserProfileViewSet, basename="user-profile")

urlpatterns = router.urls