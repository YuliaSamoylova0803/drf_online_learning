from django.db import models

from config import settings


# Create your models here.
class Course(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/images", blank=True, null=True, verbose_name="Превью курса"
    )
    description = models.TextField(null=True, blank=True, verbose_name="Описание курса")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}: {self.description}"


class Lesson(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="materials/lessons/previews/%Y/%m/%d",
        blank=True,
        null=True,
        verbose_name="Превью урока",
    )
    description = models.TextField(
        max_length=1000, null=True, blank=True, verbose_name="Описание урока"
    )
    link_to_the_video = models.URLField(
        verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео урока"
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец")

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title}: {self.description}"


class Subscribe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'{self.user} - {self.course}'
