from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrStaff
from .models import User, Payment
from .serializers import (
    UserProfileSerializer,
    PaymentSerializer,
    UserSerializer,
    OtherUserProfileSerializer,
)
from rest_framework.response import Response


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
