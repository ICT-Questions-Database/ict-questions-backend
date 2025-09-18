from apps.questions.models import Question, Alternative, CorrectAnswersSources
from rest_framework.serializers import ModelSerializer


class AlternativeSerializer(ModelSerializer):
    class Meta:
        model = Alternative
        fields = [
            "id",
            "question",
            "text",
            "is_correct"
        ]


class QuestionSerializer(ModelSerializer):
    alternatives = AlternativeSerializer(many=True, read_only=True)

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
            "alternatives"
        ]


class CorrectAnswersSourcesSerializer(ModelSerializer):
    class Meta:
        model = CorrectAnswersSources
        fields = [
            "id",
            "alternative",
            "source"
        ]
