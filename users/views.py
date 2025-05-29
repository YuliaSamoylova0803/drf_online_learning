from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .permissions import IsOwnerOrStaff
from .models import User, Payment
from .serializers import (
    UserProfileSerializer,
    PaymentSerializer,
    UserSerializer,
    OtherUserProfileSerializer,
)
from rest_framework.response import Response

from .services import create_payment_link


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related("payments")
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrStaff]

    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user

    def list(self, request, *args, **kwargs):
        """Показывает профиль текущего пользователя"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == "retrieve":
            if self.kwargs.get("pk") == str(self.request.user.pk):
                return UserProfileSerializer  # Полная информация для своего профиля
            return (
                OtherUserProfileSerializer  # Ограниченная информация для чужого профиля
            )
        return UserProfileSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Эндпоинт для получения текущего пользователя"""
        serializer = UserProfileSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]  # Бэкенд для обработки фильтра
    # Поля, по которым можно фильтровать
    filterset_fields = (
        "paid_course",  # Фильтр по ID курса
        "paid_lesson",  # Фильтр по ID урока
        "payment_method",  # Фильтр по способу оплаты (cash/transfer)
    )
    # Поля, по которым можно сортировать
    ordering_fields = ["date_of_payment", "amount"]

    # Сортировка по умолчанию (если не указан параметр `ordering`)
    ordering = ["-date_of_payment"]  # Новые платежи сначала


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SimplePaymentView(APIView):
    """Упрощенный вариант обработки платежей"""

    def post(self, request):
        # Создаем запись о платеже
        payment = Payment.objects.create(
            user=request.user,
            paid_course_id=request.data.get("course_id"),
            paid_lesson_id=request.data.get("lesson_id"),
            amount=request.data.get("amount"),
            status="pending",
        )
        # Получаем название продукта
        product_name = (
            payment.paid_course.title
            if payment.paid_course
            else payment.paid_lesson.title
        )

        # Создаем ссылку на оплату
        payment_url, payment_id = create_payment_link(
            amount=payment.amount, product_name=product_name
        )

        if not payment_url:
            payment.delete()
            return Response(
                {"error": payment_id},  # Здесь payment_id содержит текст ошибки
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Сохраняем данные платежа
        payment.link = payment_url
        payment.payment_id = payment_id
        payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "payment_url": payment_url,
                "amount": payment.amount,
                "product": product_name,
            },
            status=status.HTTP_201_CREATED,
        )
