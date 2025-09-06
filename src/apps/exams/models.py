from django.db.models import (
    Model,
    ForeignKey,
    FloatField,
    CharField,
    TextChoices,
    DateTimeField,
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

    user_id = ForeignKey(CustomUser, on_delete=CASCADE)
    grade = FloatField()
    track = CharField(max_length=50, choices=Track.choices)
    level = CharField(max_length=4, choices=Level.choices)

    start_date = DateTimeField(auto_now_add=True)
    end_date = DateTimeField(null=True, blank=True)
    duration = DateTimeField()

    def finish(self):
        """Marca a tentativa como finalizada (apos o usuario terminar)"""
        self.end_date = timezone.now()
        self.duration = self.end_date - self.start_date
        self.save()


class ExamQuestion(Model):
    exam_attempt_id = ForeignKey(ExamAttempt, on_delete=CASCADE)
    question_id = ForeignKey(Question, on_delete=CASCADE)
