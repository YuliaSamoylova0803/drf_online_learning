from django.shortcuts import render
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from rest_framework import viewsets, generics


# Create your views here.
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()



