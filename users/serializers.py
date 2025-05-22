from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from materials.serializers import CourseSerializer, LessonSerializer
from users.models import User, Payment


class PaymentHistorySerializer(serializers.ModelSerializer):
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "date_of_payment",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]


# Основной сериализатор платежей (может использоваться в других местах)
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class OtherUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "city", "avatar", "tg_nick"]
        read_only_fields = fields


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentHistorySerializer(
        many=True, read_only=True, source="payments.all"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "phone_number",
            "city",
            "avatar",
            "tg_nick",
            "payments",
        ]

        read_only_fields = ["id", "email"]


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
