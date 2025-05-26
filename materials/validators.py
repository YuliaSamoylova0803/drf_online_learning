from urllib.parse import urlparse
from rest_framework.exceptions import ValidationError


class StrictYouTubeLinkValidator:
    """Валидатор для строгой проверки URL YouTube"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field_value = dict(value).get(self.field)

        if not field_value:
            return

        parsed_url = urlparse(field_value)
        domain = parsed_url.netloc.lower()

        if not ('youtube.com' in domain or 'youtu.be' in domain):
            raise ValidationError("Разрешены только ссылки на YouTube")
