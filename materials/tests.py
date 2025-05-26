from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Course, Lesson
from users.models import User


# Create your tests here.
class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", password="123zxc", is_staff=True)
        self.course = Course.objects.create(
            title="Python: основы написания кода",
            owner=self.user
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
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.title
        )

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

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        """
        Тестирование обновление урока
        """
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title": "Типы данных"
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data["title"], "Типы данных"
        )

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
            f"Ожидался 204, получен {response.status_code}. Проверьте права доступа"
        )

        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()

        # Удаляем динамические поля перед сравнением
        for lesson in data['results']:
            lesson.pop('created_at', None)
            lesson.pop('updated_at', None)

        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [{
                "id": self.lesson.pk,
                "title": self.lesson.title,
                "preview": None,
                "description": self.lesson.description,
                "link_to_the_video": self.lesson.link_to_the_video,
                "course": self.course.pk,
                "owner": self.user.pk
            }]
        }

        self.assertEqual(data, expected)


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", password="123zxc", is_staff=True)
        self.course = Course.objects.create(
            title="Python: основы написания кода",
            owner=self.user
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
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.course.title
        )