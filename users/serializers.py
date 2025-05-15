from rest_framework import serializers
from .models import User


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number',
                  'city', 'avatar', 'tg_nick']
        read_only_fields = ['id', 'email']
