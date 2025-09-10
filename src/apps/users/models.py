from django.db.models import DateTimeField, EmailField, CharField
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = CharField(max_length=150, blank=False, null=False)
    last_name = CharField(max_length=150, blank=False, null=False)

    email = EmailField(unique=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"  # Muda o campo de login padrão para email
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]


    class Meta:
        db_table = "users"
