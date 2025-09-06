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
from apps.users.models import CustomUser
from apps.questions.models import Question
from django.utils import timezone


class ExamAttempt(Model):
    class Track(TextChoices):
        CLOUD = "cloud", "Cloud"
        NETWORK = "network", "Network"
        COMPUTING = "computing", "Computing"

    class Level(TextChoices):
        HCIA = "hcia", "HCIA"
        HCIP = "hcip", "HCIP"
        HCIE = "hcie", "HCIE"

    user = ForeignKey(CustomUser, on_delete=CASCADE)
    grade = FloatField()
    track = CharField(max_length=50, choices=Track.choices)
    level = CharField(max_length=4, choices=Level.choices)

    start_date = DateTimeField(auto_now_add=True)
    end_date = DateTimeField(null=True, blank=True)
    duration = DurationField(null=True, blank=True)

    def finish(self):
        """Marca a tentativa como finalizada (apos o usuario terminar)"""
        self.end_date = timezone.now()
        self.duration = self.end_date - self.start_date
        self.save()

    class Meta:
        db_table = "exam_attempts"


class ExamQuestion(Model):
    exam_attempt = ForeignKey(ExamAttempt, on_delete=CASCADE)
    question = ForeignKey(Question, on_delete=CASCADE)

    class Meta:
        db_table = "exam_questions"
