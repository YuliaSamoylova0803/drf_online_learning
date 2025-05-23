from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

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
        max_digits=10, decimal_places=2, verbose_name="Суммам оплаты"
    )
    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты"
    )

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
        ordering = ["-date_of_payment"]

    def __str__(self):
        return f"{self.user.email} - {self.amount} ({self.date_of_payment})"
