from django.db.models import Model, ForeignKey, DateTimeField, EmailField, CharField, CASCADE
from django.contrib.auth.models import AbstractUser
from apps.exams.models import ExamAttempt
from apps.questions.models import Question, Alternative
from django.conf import settings


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


class UserAnswers(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    exam_attempt = ForeignKey(ExamAttempt, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)
    alternative = ForeignKey(Alternative, on_delete=CASCADE)

    class Meta:
        db_table = "user_answers"