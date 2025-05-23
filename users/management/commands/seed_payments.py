from django.core.management.base import BaseCommand
from users.models import Payment
from materials.models import Course, Lesson
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Заполняет базу тестовыми платежами"

    def handle(self, *args, **options):
        # Создаем тестовых пользователей
        try:
            user1 = User.objects.create_user(
                username="user1",
                email="user1@example.com",
                password="testpass123",
                first_name="Иван",
                last_name="Иванов",
            )

            user2 = User.objects.create_user(
                username="user2",
                email="user2@example.com",
                password="testpass123",
                first_name="Петр",
                last_name="Петров",
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка создания пользователей: {e}"))
            return

        # Создаем тестовые курсы и уроки
        try:
            course = Course.objects.create(
                title="Тестовый курс", description="Описание тестового курса"
            )

            lesson = Lesson.objects.create(
                title="Тестовый урок",
                description="Описание тестового урока",
                link_to_the_video="https://example.com/video1",
                course=course,
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка создания курса/урока: {e}"))
            return

        # Создаем платежи
        payments_data = [
            {
                "user": user1,
                "paid_course": course,
                "paid_lesson": None,
                "amount": "5000.00",
                "payment_method": "transfer",
            },
            {
                "user": user2,
                "paid_course": None,
                "paid_lesson": lesson,
                "amount": "1500.00",
                "payment_method": "cash",
            },
        ]

        for payment in payments_data:
            try:
                Payment.objects.create(**payment)
                self.stdout.write(
                    self.style.SUCCESS(f'Создан платеж для {payment["user"].email}')
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка создания платежа: {e}"))

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
