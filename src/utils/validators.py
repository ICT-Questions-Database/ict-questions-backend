from apps.users.models import User
from rest_framework.exceptions import ValidationError


def validate_unique_email(value: str) -> str:
    if User.objects.filter(email=value).exists():
        raise ValidationError(detail="Email inválido.", code="invalid")
    return value
