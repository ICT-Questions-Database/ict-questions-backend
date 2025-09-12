from apps.questions.models import Question, Alternative, CorrectAnswersSources
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

class AlternativeSerializer(ModelSerializer):
    class Meta:
        model = Alternative
        fields = [
            "id",
            "question",
            "text",
            "is_correct"
        ]

class CorrectAnswersSourcesSerializer(ModelSerializer):
    class Meta:
        model = CorrectAnswersSources
        fields = [
            "question",
            "source"
        ]