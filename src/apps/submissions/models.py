from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    TextField,
    URLField,
    BooleanField,
    FloatField,
    DateTimeField,
    SET_NULL,
    CASCADE
)
from django.conf import settings
from utils.enums import Track, Level, Status


class QuestionSubmission(Model):
    submitted_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, null=True, related_name="submitted_questions")
    reviewed_by = ForeignKey(settings.AUTH_USER_MODEL, on_delete=SET_NULL, blank=True, null=True, related_name="reviewed_questions")
    text = TextField()
    track = CharField(max_length=50, choices=Track.choices)
    level = CharField(max_length=4, choices=Level.choices)
    status = CharField(choices=Status.choices)
    weight = FloatField()
    feedback = TextField(blank=True, null=True)
    has_answer = BooleanField(default=False)
    has_multiple_answers = BooleanField(default=False)

    sent_at = DateTimeField(auto_now_add=True)
    reviewed_at = DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "question_submissions"


class AlternativeSubmission(Model):
    question_submission = ForeignKey(QuestionSubmission, on_delete=CASCADE, related_name="alternatives")
    text = TextField()
    is_correct = BooleanField()

    class Meta:
        db_table = "alternative_submissions"

class CorrectSubmissionAnswersSources(Model):
    alternative_submission = ForeignKey(AlternativeSubmission, on_delete=CASCADE)
    source = URLField(max_length=200)

    class Meta:
        db_table = "correct_submission_answer_sources"
