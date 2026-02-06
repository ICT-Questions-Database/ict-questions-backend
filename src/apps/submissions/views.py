from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import (
    QuestionSubmission,
    CorrectSubmissionAnswersSources,
    AlternativeSubmission,
)
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
from .schemas import (
    question_submissions_schema,
    correct_submissions_answers_sources_schema,
    alternative_submissions_schema,
)
from utils.pagination import StandardResultsSetPagination


@question_submissions_schema
class QuestionSubmissionViewset(ModelViewSet):
    queryset = QuestionSubmission.objects.all().order_by("-id")
    serializer_class = QuestionSubmissionSerializer
    # permission_classes = [IsAuthenticated, QuestionSubmissionPermission]
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = QuestionSubmission.objects.all()
        else:
            queryset = QuestionSubmission.objects.filter(submitted_by=user)

        queryset = queryset.prefetch_related("alternatives")

        return queryset.order_by("-id")

    # def perform_create(self, serializer):
    #     serializer.save(submitted_by=self.request.user)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsAdminUser],
    )
    def review(self, request, pk=None):
        submission = self.get_object()

        submission = review_submission(
            submission=submission,
            reviewer=request.user,
            status=request.data.get("status"),
            feedback=request.data.get("feedback"),
        )

        serializer = self.get_serializer(submission)
        return Response(serializer.data)


@correct_submissions_answers_sources_schema
class CorrectSubmissionAnswersSourcesViewSet(ModelViewSet):
    queryset = CorrectSubmissionAnswersSources.objects.all().order_by("-id")
    serializer_class = CorrectSubmissionAnswersSourcesSerializer
    # permission_classes = [IsAuthenticated, BaseSubmissionPermission]
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_submission_id")
        return get_sources_for_user(
            self.request.user, question_submission_id=question_id
        )


@alternative_submissions_schema
class AlternativeSubmissionViewSet(ModelViewSet):
    queryset = AlternativeSubmission.objects.all().order_by("-id")
    serializer_class = AlternativeSubmissionSerializer
    # permission_classes = [IsAuthenticated, BaseSubmissionPermission]
    pagination_class = StandardResultsSetPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_submission_id")
        return get_alternatives_for_questions_by_user(
            self.request.user, question_submission_id=question_id
        )
