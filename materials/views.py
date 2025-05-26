from rest_framework.permissions import IsAuthenticated, AllowAny

from users.permissions import IsModerPermission, IsOwnerOrStaff
from .models import Course, Lesson, Subscribe
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,

)
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .paginators import MaterialsPaginator


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerPermission]
        elif self.action == "destroy":
            self.permission_classes = [
                IsAuthenticated,
                # ~IsModerPermission,
                IsOwnerOrStaff,
            ]
        elif self.action in ["update", "partial_update"]:
            self.permission_classes = [
                IsAuthenticated,
                IsModerPermission | IsOwnerOrStaff,
            ]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.kwargs.get("course_id")
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    action = "retrieve"
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerPermission | IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    action = "update"
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerPermission | IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        print("Delete operation requested by:", self.request.user)
        return super().get_queryset()

    def perform_destroy(self, instance):
        # Дополнительные проверки перед удалением
        super().perform_destroy(instance)


class SubscriptionAPIView(APIView):
    """Управление подписками на курсы"""

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        subscription = Subscribe.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscribe.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message}, status=status.HTTP_200_OK)
