from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import QuestionSubmission, AlternativeSubmission, CorrectSubmissionAnswersSources
from .serializers import (
    QuestionSubmissionSerializer,
    CorrectSubmissionAnswersSourcesSerializer,
    AlternativeSubmissionSerializer,
)
from .permissions import (
    QuestionSubmissionPermission,
    BaseSubmissionPermission,
)
from .services import (
    review_submission,
    get_sources_for_user,
    get_alternatives_for_questions_by_user,
)
from .pagination import SubmissionPagination
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        summary="Lists a set of question_submissions",
        description="Lists all question_submissions if the user is an admin; otherwise, returns only the question submissions submitted by the user",
        tags=["question_submissions"],
    ),
    retrieve=extend_schema(
        summary="Retrieve a question_submission object",
        description="Retrieve a question_submission object",
        tags=["question_submissions"],
    ),
    create=extend_schema(
        summary="Creates a question_submission object",
        description="Creates a question_submission_object.",
        tags=["question_submissions"],
    ),
    update=extend_schema(
        summary="Updates a question_submission object",
        description="Updates a question_submission object.",
        tags=["question_submissions"],
    ),
    partial_update=extend_schema(
        summary="Partially updates a question_submission instance",
        description="Partially updates a question_submission instance",
        tags=["question_submissions"],
    ),
    review=extend_schema(
        summary="Updates a reviewed question in the database.",
        description="Updates a reviewed question in the database, populating submitted_by.",
        tags=["question_submissions"],
    ),
    destroy=extend_schema(
        summary="Deletes a question_submission object",
        description="Deletes a question_submission object.",
        tags=["question_submissions"],
    ),
)
class QuestionSubmissionViewset(ModelViewSet):
    queryset = QuestionSubmission.objects.none()
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


@extend_schema_view(
    list=extend_schema(
        summary="Lists all CorrectSubmissionAnswersSources from the user",
        description="Lists all CorrectSubmissionAnswersSources from the user",
        tags=["correct_submission_answers_sources"],
    ),
    retrieve=extend_schema(
        summary="Retrieves a CorrectSubmissionAnswersSources submitted by the user",
        description="Retrieves a CorrectSubmissionAnswersSources submitted by the user",
        tags=["correct_submission_answers_sources"],
    ),
    create=extend_schema(
        summary="Creates a CorrectSubmissionAnswersSources object",
        description="Creates a CorrectSubmissionAnswersSources in the database.",
        tags=["correct_submission_answers_sources"],
    ),
    update=extend_schema(
        summary="Updates a CorrectSubmissionAnswersSources object",
        description="Updates a CorrectSubmissionAnswersSources object",
        tags=["correct_submission_answers_sources"],
    ),
    destroy=extend_schema(
        summary="Deletes a CorrectSubmissionAnswersSources object",
        description="Deletes a CorrectSubmissionAnswersSources object in the database.",
        tags=["correct_submission_answers_sources"],
    ),
)
class CorrectSubmissionAnswersSourcesViewSet(ModelViewSet):
    queryset = CorrectSubmissionAnswersSources.objects.none()
    serializer_class = CorrectSubmissionAnswersSourcesSerializer
    permission_classes = [IsAuthenticated, BaseSubmissionPermission]
    pagination_class = SubmissionPagination
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_submission_id")
        return get_sources_for_user(
            self.request.user, question_submission_id=question_id
        )


@extend_schema_view(
    list=extend_schema(
        summary="Lists all AlternativeSubmission from the user",
        description="Lists all AlternativeSubmission from the user",
        tags=["alternative_submissions"],
    ),
    retrieve=extend_schema(
        summary="Retrieves a AlternativeSubmission submitted by the user",
        description="Retrieves a AlternativeSubmission submitted by the user",
        tags=["alternative_submissions"],
    ),
    create=extend_schema(
        summary="Creates a AlternativeSubmission object",
        description="Creates a AlternativeSubmission in the database.",
        tags=["alternative_submissions"],
    ),
    update=extend_schema(
        summary="Updates a AlternativeSubmission object",
        description="Updates a AlternativeSubmission object",
        tags=["alternative_submissions"],
    ),
    partial_update=extend_schema(
        summary="Partially updates a AlternativeSubmission object",
        description="Partially updates a AlternativeSubmission object",
        tags=["alternative_submissions"],
    ),
    destroy=extend_schema(
        summary="Deletes a AlternativeSubmission object",
        description="Deletes a AlternativeSubmission object in the database.",
        tags=["alternative_submissions"],
    ),
)
class AlternativeSubmissionViewSet(ModelViewSet):
    queryset = AlternativeSubmission.objects.none()
    serializer_class = AlternativeSubmissionSerializer
    permission_classes = [IsAuthenticated, BaseSubmissionPermission]
    pagination_class = SubmissionPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_submission_id")
        return get_alternatives_for_questions_by_user(
            self.request.user, question_submission_id=question_id
        )
