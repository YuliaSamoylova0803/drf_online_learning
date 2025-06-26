from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


@shared_task
def block_inactive_users():
    """Блокирует пользователей, не заходивших более месяца"""
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)  # Исправлено здесь

    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    count = inactive_users.count()
    inactive_users.update(is_active=False)

    return f"Deactivated {count} inactive users"
