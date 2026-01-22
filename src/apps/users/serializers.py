from rest_framework.serializers import ModelSerializer
from .models import User, UserAnswers


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserRetrieveSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
        ]


class UserPatchSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
        ]
        read_only_fields = ["id", "email"]


class UserAnswersSerializer(ModelSerializer):
    class Meta:
        model = UserAnswers
        fields = "__all__"

