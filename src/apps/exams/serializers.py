from rest_framework.serializers import ModelSerializer, CharField
from .models import ExamAttempt, ExamQuestion

class ExamAttemptSerializer(ModelSerializer):
    track_display = CharField(source="get_track_display", read_only=True)
    level_display = CharField(source="get_level_display", read_only=True)

    class Meta:
        model = ExamAttempt
        fields = [
            "id",
            "user",
            "grade",
            "track",
            "track_display",
            "level",
            "level_display",
            "start_date",
            "end_date",
            "duration",
        ]
        read_only_fields = ["start_date", "end_date", "duration", "track_display", "level_display"]


class ExamQuestion(ModelSerializer):
    class Meta:
        model = ExamQuestion
        fields = "__all__"