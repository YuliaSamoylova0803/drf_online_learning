from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from materials.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(
        unique=True, verbose_name="Электронный адрес", help_text="Введите свою почту"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Родной город",
        help_text="Введите город, в котором проживаете",
    )
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        verbose_name="Изображение пользователя",
        help_text="Изображение должно быть квадратным (рекомендуемый размер 200x200)",
    )
    tg_nick = models.CharField(
        max_length=50,
        verbose_name="Ник телеграмм",
        blank=True,
        null=True,
        help_text="Введите ник телеграмм",
    )

    token = models.CharField(
        max_length=100, verbose_name="Token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return f"{self.username} {self.email})"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cash", "Наличные"),
        ("transfer", "Перевод на счет"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачено"),
        ("failed", "Ошибка оплаты"),
        ("refunded", "Возврат"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    date_of_payment = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата платежа"
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
        validators=[MinValueValidator(0)],
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )
    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        verbose_name="Статус платежа",
    )
    payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID платежа в системе",
        unique=True,
    )
    link = models.URLField(
        max_length=400,
        null=True,
        blank=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["-date_of_payment"]

    def clean(self):
        if self.paid_course and self.paid_lesson:
            raise ValidationError(
                "Платеж может быть привязан только к курсу ИЛИ к уроку, но не к обоим одновременно"
            )
        if not self.paid_course and not self.paid_lesson:
            raise ValidationError(
                "Платеж должен быть привязан либо к курсу, либо к уроку"
            )

    @property
    def payment_for(self):
        if self.paid_course:
            return f"Курс: {self.paid_course.title}"
        elif self.paid_lesson:
            return f"Урок: {self.paid_lesson.title} (Курс: {self.paid_lesson.course.title})"
        return "Не указано"

    def __str__(self):
        items = []
        if self.paid_course:
            items.append(f"курс {self.paid_course.title}")
        if self.paid_lesson:
            items.append(f"урок {self.paid_lesson.title}")

        subject = " и ".join(items) if items else "не указано"
        return f"Платеж {self.amount} от {self.user.email} за {subject} ({self.date_of_payment})"
