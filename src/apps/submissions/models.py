from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    TextField,
    BooleanField,
    FloatField,
    DateTimeField,
    TextChoices,
    SET_NULL,
)
from apps.users.models import CustomUser


class QuestionSubmission(Model):
    class Track(TextChoices):
        CLOUD = "cloud", "Cloud"
        NETWORK = "network", "Network"
        COMPUTING = "computing", "Computing"

    class Level(TextChoices):
        HCIA = "hcia", "HCIA"
        HCIP = "hcip", "HCIP"
        HCIE = "hcie", "HCIE"

    class Status(TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    submitted_by = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name="submitted_questions")
    reviewed_by = ForeignKey(CustomUser, on_delete=SET_NULL, blank=True, null=True, related_name="reviewed_questions")
    text = TextField()
    track = CharField(max_length=50, choices=Track.choices)
    level = CharField(max_length=4, choices=Level.choices)
    status = CharField(choices=Status.choices)
    weight = FloatField()
    feedback = FloatField()
    has_answer = BooleanField(default=False)
    has_multiple_answers = BooleanField(default=False)

    sent_at = DateTimeField(auto_now_add=True)
    reviewed_at = DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "question_submissions"
