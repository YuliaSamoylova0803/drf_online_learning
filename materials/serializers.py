from dataclasses import field

from rest_framework import serializers
from .models import Course, Lesson
from .validators import StrictYouTubeLinkValidator

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
        validators = [
            StrictYouTubeLinkValidator(field="link_to_the_video"),
        ]

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "preview",
            "description",
            "created_at",
            "updated_at",
            "lessons_count",  # Добавляем новое поле в список полей
            "lessons",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "lessons_count",
        ]  # Делаем поле только для чтения

    def get_lessons_count(self, instance):
        """Возвращает количество уроков в курсе"""
        return (
            instance.lessons.count()
        )  # Используем related_name 'lessons' из модели Lesson
