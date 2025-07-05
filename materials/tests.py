from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Course, Lesson, Subscribe
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com", password="123zxc", is_staff=True
        )
        self.course = Course.objects.create(
            title="Python: основы написания кода", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Алгоритм",
            course=self.course,
            description="Чёткая последовательность действий для достижения результата",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """
        Тестирование извлечение урока
        """
        url = reverse("materials:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """
        Тестирование создание урока
        """
        url = reverse("materials:lesson-create")
        data = {
            "title": "Типы данных",
            "link_to_the_video": "https://www.youtube.com/watch?v=valid_video_id",
            "course": self.course.id,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """
        Тестирование обновление урока
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Типы данных"}
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Типы данных")

    def test_lesson_delete(self):
        """
        Тестирование удаление урока
        """
        initial_count = Lesson.objects.count()
        self.assertEqual(initial_count, 1)
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))

        response = self.client.delete(url)

        # Проверяем статус
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Ожидался 204, получен {response.status_code}. Проверьте права доступа",
        )

        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()

        # Удаляем динамические поля перед сравнением
        for lesson in data["results"]:
            lesson.pop("created_at", None)
            lesson.pop("updated_at", None)

        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "preview": None,
                    "description": self.lesson.description,
                    "link_to_the_video": self.lesson.link_to_the_video,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(data, expected)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="admin@example.com", password="123zxc", is_staff=True
        )
        self.course = Course.objects.create(
            title="Python: основы написания кода", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Алгоритм",
            course=self.course,
            description="Чёткая последовательность действий для достижения результата",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """
        Тестирование извлечение курса
        """
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    # def test_course_create(self):
    #     """
    #     Тестирование создание курса
    #     """
    #     url = reverse("materials:courses-list")
    #     data = {"title": "Основы синтаксиса"}
    #     response = self.client.post(url, data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """
        Тестирование обновление курса
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {"title": "Списки"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Списки")

    def test_course_delete(self):
        """
        Тестирование удаление курса
        """
        self.assertEqual(self.course.owner, self.user)

        initial_count = Course.objects.count()
        self.assertEqual(initial_count, 1)
        url = reverse("materials:courses-detail", args=(self.course.pk,))

        response = self.client.delete(url)

        # Проверяем статус
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Ожидался 204, получен {response.status_code}. Проверьте права доступа",
        )

        self.assertEqual(Course.objects.count(), 0)

    def test_course_list(self):
        """
        Тестирование листа курса
        :return:
        """
        url = reverse("materials:courses-list")
        response = self.client.get(url)
        data = response.json()

        # Удаляем динамические поля перед сравнением
        for course in data["results"]:
            course.pop("created_at", None)
            course.pop("updated_at", None)

        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "is_subscribed": False,
                    "title": self.course.title,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk,
                },
            ],
        }

        self.assertEqual(data, expected)


class SubscribeTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователей с уникальными email и username
        self.user = User.objects.create_user(
            email="user@example.com",
            password="123zxc",
            username="user1",  # Уникальное имя пользователя
            is_staff=True,
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="123zxc",
            username="user2",  # Уникальное имя пользователя
        )
        self.course = Course.objects.create(
            title="Python: основы написания кода", owner=self.user
        )
        self.course2 = Course.objects.create(
            title="Django: основы", owner=self.other_user
        )
        self.subscribe_url = reverse("materials:subscription")
        self.client.force_authenticate(user=self.user)

    def test_subscribe_create(self):
        """
        Тестирование создание подписки
        """

        response = self.client.post(
            self.subscribe_url, {"course_id": self.course.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscribe.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscribe_delete(self):
        """
        Тестирование удаления подписки
        """
        # Сначала создаем подписку
        Subscribe.objects.create(user=self.user, course=self.course)
        # Затем удаляем ее
        response = self.client.post(
            self.subscribe_url, {"course_id": self.course.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(
            Subscribe.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscribe_unauthorized(self):
        """
        Тестирование попытки подписки неавторизованным пользователем
        """
        self.client.logout()  # Разлогиниваем пользователя
        response = self.client.post(
            self.subscribe_url, {"course_id": self.course.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscribe_to_other_user_course(self):
        """
        Тестирование подписки на курс другого пользователя
        """
        response = self.client.post(
            self.subscribe_url,
            {"course_id": self.course2.id},  # Курс принадлежит other_user
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(
            Subscribe.objects.filter(user=self.user, course=self.course2).exists()
        )

    def test_subscribe_twice(self):
        """
        Тестирование двойной подписки на один курс
        """

        response1 = self.client.post(
            self.subscribe_url, {"course_id": self.course.id}, format="json"
        )

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.data["message"], "Подписка добавлена")

        # Вторая попытка подписаться на тот же курс
        response2 = self.client.post(
            self.subscribe_url, {"course_id": self.course.id}, format="json"
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["message"], "Подписка удалена")
