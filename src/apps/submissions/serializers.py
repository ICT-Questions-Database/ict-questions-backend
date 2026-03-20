from rest_framework.serializers import ModelSerializer
from .models import (
    QuestionSubmission,
    CorrectSubmissionAnswersSources,
    AlternativeSubmission,
)


class AlternativeSubmissionSerializer(ModelSerializer):
    class Meta:
        model = AlternativeSubmission
        fields = "__all__"


class QuestionSubmissionSerializer(ModelSerializer):
    alternatives = AlternativeSubmissionSerializer(many=True, read_only=True)

    class Meta:
        model = QuestionSubmission
        fields = [
            "id",
            "submitted_by",
            "reviewed_by",
            "text",
            "track",
            "level",
            "status",
            "weight",
            "feedback",
            "has_answer",
            "has_multiple_answers",
            "sent_at",
            "reviewed_at",
            "alternatives",
        ]
        read_only_fields = [
            "id",
            "submitted_by",
            "reviewed_by",
            "sent_at",
            "reviewed_at",
            "alternatives",
        ]


class CorrectSubmissionAnswersSourcesSerializer(ModelSerializer):
    class Meta:
        model = CorrectSubmissionAnswersSources
        fields = "__all__"
