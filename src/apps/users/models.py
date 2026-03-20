from django.db.models import (
    Model,
    ForeignKey,
    DateTimeField,
    EmailField,
    CharField,
    BooleanField,
    CASCADE,
)
from apps.exams.models import ExamAttempt
from apps.questions.models import Question, Alternative
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Cria e salva um usuário com o email e senha fornecidos.
        """
        if not email:
            raise ValueError("O email é obrigatório")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o email e senha fornecidos.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    name = CharField(max_length=256)
    email = EmailField(unique=True)

    is_staff = BooleanField(
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = BooleanField(
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class User(AbstractUser):
    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email


class UserAnswers(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    exam_attempt = ForeignKey(ExamAttempt, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)
    alternative = ForeignKey(Alternative, on_delete=CASCADE)

    class Meta:
        db_table = "user_answers"
