from apps.questions.models import Question
from rest_framework.serializers import ModelSerializer


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = [
            "id",
            "submitted_by",
            "reviewed_by",
            "text",
            "level",
            "has_answer",
            "has_multiple_answers",
            "track",
            "weight",
        ]