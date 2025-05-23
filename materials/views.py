from rest_framework.permissions import IsAuthenticated, AllowAny

from users.permissions import IsModerPermission, IsOwnerOrStaff
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
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerPermission]
        elif self.action == "destroy":
            self.permission_classes = [
                IsAuthenticated,
                ~IsModerPermission,
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

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.kwargs.get("course_id")
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerPermission | IsOwnerOrStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerPermission | IsOwnerOrStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~IsModerPermission, IsOwnerOrStaff]
