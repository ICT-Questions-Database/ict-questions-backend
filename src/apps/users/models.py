from django.db.models import CharField, BooleanField, DateTimeField, EmailField
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    enrollment = CharField(max_length=50, unique=True)
    formation = CharField(max_length=100)

    isAdmin = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  # Muda o campo de login padrão para email
    REQUIRED_FIELDS = [
        "username"
    ]  # username passa a ser obrigatório, mas email é usado pra login

    email = EmailField(unique=True)

    class Meta:
        db_table = "users"
