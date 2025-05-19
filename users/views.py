from os import getenv

from django.core.serializers import serialize
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter

from .models import User, Payment
from .serializers import UserProfileSerializer, PaymentHistorySerializer, PaymentSerializer
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related("payments")
    serializer_class = UserProfileSerializer

    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user

    def list(self, request, *args, **kwargs):
        """Показывает профиль текущего пользователя"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Бэкенд для обработки фильтра
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