from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.models import Payment
from .models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ['created_at', 'updated_at']


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
            "lessons"
        ]
        read_only_fields = ["created_at", "updated_at", "lessons_count"]  # Делаем поле только для чтения

    def get_lessons_count(self,instance):
        """Возвращает количество уроков в курсе"""
        return instance.lessons.count() # Используем related_name 'lessons' из модели Lesson


class PaymentSerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'user',
            'date_of_payment',
            'paid_course',
            'paid_lesson',
            'amount',
            'payment_method'
        ]
        read_only_fields = ['payment_date']
