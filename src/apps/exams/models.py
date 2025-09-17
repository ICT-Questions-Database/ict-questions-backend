from django.db.models import (
    Model,
    ForeignKey,
    FloatField,
    CharField,
    TextChoices,
    DateTimeField,
    DurationField,
    CASCADE,
)
from apps.questions.models import Question
from django.conf import settings


class ExamAttempt(Model):
    class Track(TextChoices):
        CLOUD = "cloud", "Cloud"
        NETWORK = "network", "Network"
        COMPUTING = "computing", "Computing"

    class Level(TextChoices):
        HCIA = "hcia", "HCIA"
        HCIP = "hcip", "HCIP"
        HCIE = "hcie", "HCIE"

    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    grade = FloatField()
    track = CharField(max_length=50, choices=Track.choices)
    level = CharField(max_length=4, choices=Level.choices)

    start_date = DateTimeField(auto_now_add=True)
    end_date = DateTimeField(null=True, blank=True)
    duration = DurationField(null=True, blank=True)

    class Meta:
        db_table = "exam_attempts"


class ExamQuestion(Model):
    exam_attempt = ForeignKey(ExamAttempt, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)

    class Meta:
        db_table = "exam_questions"
