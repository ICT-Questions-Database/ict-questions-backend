from django.shortcuts import render
from apps.questions.serializers import QuestionSerializer
from .models import Question
from .pagination import QuestionsPagination

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_spectacular.utils import extend_schema_view, extend_schema

@extend_schema_view(
    list=extend_schema(
        summary="Lists questions",
        description="Lists questions"
    ),
    create=extend_schema(
        summary="Creates a question object",
        description="Creates a new question object.",
    ),
    destroy=extend_schema(
        summary="Deletes a question object",
        description="Deletes a question object"
    ),
    update=extend_schema(
        summary="Updates a question object",
        description="Updates a question object"
    ),
    partial_update=extend_schema(
        summary="Partially updates a question object",
        description="Partially updates a question object"
    ),
)
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = QuestionsPagination
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get_permissions(self):
        if self.action in ("post", "destroy", "put", "patch"):
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(reviewed_by=self.request.user)