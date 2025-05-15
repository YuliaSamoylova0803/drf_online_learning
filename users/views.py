from os import getenv

from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserProfileSerializer
from rest_framework.response import Response


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        """Возвращает текущего пользователя"""
        return self.request.user

    def list(self, request, *args, **kwargs):
        """Показывает профиль текущего пользователя"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
