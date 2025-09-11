from django.shortcuts import render
from apps.questions.serializers import QuestionSerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    create=extend_schema(
        summary="Creates a question object",
        description="Creates a new question object.",
    ),
)
class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put"]

    def perform_create(self, serializer):
        serializer.save(reviewed_by=self.request.user)