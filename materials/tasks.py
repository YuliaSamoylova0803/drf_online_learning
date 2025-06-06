from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Subscribe
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_course_update_notification(course_id):
    try:
        subscriptions = Subscribe.objects.filter(course_id=course_id).select_related("user")
        for subscription in subscriptions:
            send_mail(
                subject='Обновление материалов курса',
                message='Курс, на который вы подписаны, был обновлен. Проверьте новые материалы!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[subscription.user.email],
                fail_silently=False,
            )
    except Exception as e:
        logger.error(f"Error sending course update notifications: {str(e)}")