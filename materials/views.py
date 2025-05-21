from django.shortcuts import render

from users.permissions import IsModerPermission
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from rest_framework import viewsets, generics


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModerPermission,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerPermission,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
