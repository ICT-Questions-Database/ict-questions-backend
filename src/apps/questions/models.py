from django.conf import settings

from django.db.models import (
    Model,
    ForeignKey,
    DateTimeField,
    DecimalField,
    CharField,
    TextField,
    URLField,
    TextChoices,
    BooleanField,
    SET_NULL,
    CASCADE,
)


class Question(Model):
    class Level(TextChoices):
        HCIA = "HCIA"
        HCIP = "HCIP"
        HCIE = "HCIE"

    class Track(TextChoices):
        CLOUD = "Cloud"
        NETWORK = "Network"
        COMPUTING = "Computing"

    submitted_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name="user")
    reviewed_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name="reviewer")

    text = TextField()
    level = CharField(max_length=4, choices=Level.choices)
    has_answer = BooleanField()
    has_multiple_answers = BooleanField()
    track = CharField(max_length=16, choices=Track.choices)
    weight = DecimalField(max_digits=6, decimal_places=2)

    approved_at = DateTimeField(auto_now_add=True)
    last_update = DateTimeField(auto_now=True)

    class Meta:
        db_table = "questions"


class Alternative(Model):
    question = ForeignKey(Question, on_delete=CASCADE, related_name="alternatives")
    text = TextField()
    is_correct = BooleanField()

    class Meta:
        db_table = "alternatives"


class CorrectAnswersSources(Model):
    alternative = ForeignKey(Alternative, on_delete=CASCADE, related_name="sources")
    source = URLField()

    class Meta:
        db_table = "correct_answers_sources"
