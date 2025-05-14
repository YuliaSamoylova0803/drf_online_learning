from materials.apps import MaterialsConfig
from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import CourseViewSet

app_name = MaterialsConfig.name


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename="courses")


urlpatterns = [

]