from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import QuestionSubmission
from .serializers import (
    QuestionSubmissionSerializer,
    CorrectSubmissionAnswersSourcesSerializer,
    AlternativeSubmissionSerializer,
)
from .permissions import (
    QuestionSubmissionPermission,
    BaseSubmissionPermission,
)
from .services import review_submission, get_sources_for_user, get_alternatives_for_questions_by_user
from .pagination import SubmissionPagination
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="Lists a set of question_submissions",
        description="Lists all question_submissions if the user is an admin; otherwise, returns only the question submissions submitted by the user",
    ),
    retrieve=extend_schema(
        summary="Retrieve a question_submission object",
        description="Retrieve a question_submission object",
    ),
    create=extend_schema(
        summary="Creates a question_submission object",
        description="Creates a question_submission_object.",
    ),
    update=extend_schema(
        summary="Updates a question_submission object",
        description="Updates a question_submission object.",
    ),
    partial_update=extend_schema(
        summary="Partially updates a question_submission instance",
        description="Partially updates a question_submission instance",
    ),
    review=extend_schema(
        summary="Updates a reviewed question in the database.",
        description="Updates a reviewed question in the database, populating submitted_by.",
    ),
    destroy=extend_schema(
        summary="Deletes a question_submission object",
        description="Deletes a question_submission object.",
    ),
)
class QuestionSubmissionViewset(ModelViewSet):
    serializer_class = QuestionSubmissionSerializer
    permission_classes = [IsAuthenticated, QuestionSubmissionPermission]
    pagination_class = SubmissionPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return QuestionSubmission.objects.all().order_by("id")
        return QuestionSubmission.objects.filter(submitted_by=user).order_by("id")

    def perform_create(self, serializer):
        serializer.save(submitted_by=self.request.user)

    @action(detail=True, methods=["patch"])
    def review(self, request, pk=None):
        submission = self.get_object()
        status = request.data.get("status")
        feedback = request.data.get("feedback", None)

        try:
            submission = review_submission(submission, request.user, status, feedback)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=403)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        serializer = self.get_serializer(submission)
        return Response(serializer.data)


class CorrectSubmissionAnswersSourcesViewSet(ModelViewSet):
    serializer_class = CorrectSubmissionAnswersSourcesSerializer
    permission_classes = [IsAuthenticated, BaseSubmissionPermission]
    pagination_class = SubmissionPagination
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_submission_id")
        return get_sources_for_user(
            self.request.user, question_submission_id=question_id
        )


class AlternativeSubmissionViewSet(ModelViewSet):
    serializer_class = AlternativeSubmissionSerializer
    permission_classes = [IsAuthenticated, BaseSubmissionPermission]
    pagination_class = SubmissionPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_submission_id")
        return get_alternatives_for_questions_by_user(
            self.request.user, question_submission_id=question_id
        )
    