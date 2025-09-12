from rest_framework.serializers import ModelSerializer
from .models import QuestionSubmission, CorrectSubmissionAnswersSources

class QuestionSubmissionSerializer(ModelSerializer):
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
        ]
        read_only_fields = [
            "submitted_by",
            "reviewed_by",
            "sent_at",
            "reviewed_at",
        ]


class CorrectSubmissionAnswersSourcesSerializer(ModelSerializer):
    class Meta:
        model = CorrectSubmissionAnswersSources
        fields = "__all__"
