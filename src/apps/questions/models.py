from apps.users.models import CustomUser

from django.db.models import (
    Model,
    ForeignKey,
    DateTimeField,
    DecimalField,
    CharField,
    TextField,
    TextChoices,
    BooleanField,
    SET_NULL,
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

    submitted_by = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name="user")
    reviewed_by = ForeignKey(CustomUser, on_delete=SET_NULL, null=True, related_name="reviewer")

    text = TextField()
    level = CharField(max_length=4)
    has_answer = BooleanField()
    has_multiple_answers = BooleanField()
    track = CharField(max_length=16)
    weight = DecimalField(max_digits=6, decimal_places=2)

    approved_at = DateTimeField(auto_now_add=True)
    last_update = DateTimeField(auto_now=True)

    class Meta:
        db_table = "questions"
