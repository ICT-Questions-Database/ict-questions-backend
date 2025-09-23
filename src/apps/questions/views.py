from apps.questions.serializers import QuestionSerializer, AlternativeSerializer, CorrectAnswersSourcesSerializer
from .models import Question, Alternative, CorrectAnswersSources
from .pagination import QuestionsPagination

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(
        summary="List questions",
        description="Retrieve a paginated list of questions."
    ),
    create=extend_schema(
        summary="Create a question",
        description="Create a new question object."
    ),
    retrieve=extend_schema(
        summary="Retrieve a question",
        description="Retrieve a single question by its ID."
    ),
    destroy=extend_schema(
        summary="Delete a question",
        description="Delete a question object by its ID."
    ),
    update=extend_schema(
        summary="Update a question",
        description="Update all fields of a question object."
    ),
    partial_update=extend_schema(
        summary="Partially update a question",
        description="Update some fields of a question object."
    ),
)
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().order_by("id")
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = QuestionsPagination
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser] if self.action in ("create", "destroy", "update", "partial_update") else [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(reviewed_by=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="List alternatives",
        description="Retrieve a list of alternatives. Staff users may filter by question ID using the `?question_id=` parameter.",
        tags=["alternatives"]
    ),
    create=extend_schema(
        summary="Create an alternative",
        description="Create a new alternative object.",
        tags=["alternatives"]
    ),
    retrieve=extend_schema(
        summary="Retrieve an alternative",
        description="Retrieve a single alternative by its ID.",
        tags=["alternatives"]
    ),
    destroy=extend_schema(
        summary="Delete an alternative",
        description="Delete an alternative object by its ID.",
        tags=["alternatives"]
    ),
    update=extend_schema(
        summary="Update an alternative",
        description="Update all fields of an alternative object.",
        tags=["alternatives"]
    ),
    partial_update=extend_schema(
        summary="Partially update an alternative",
        description="Update some fields of an alternative object.",
        tags=["alternatives"]
    ),
)
class AlternativeViewSet(ModelViewSet):
    serializer_class = AlternativeSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "put", "delete", "patch"]
 
    queryset = Alternative.objects.all()
 
    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsAdminUser] if self.action in ("create", "destroy", "update", "partial_update") else [IsAuthenticated]
        return [permission() for permission in permission_classes]


@extend_schema_view(
    list=extend_schema(
        summary="List correct answer sources",
        description="Retrieve a list of sources for correct answers. Staff users may filter by question ID using the `?question_id=` parameter.",
        tags=["correct_answers_sources"]
    ),
    create=extend_schema(
        summary="Create a correct answer source",
        description="Create a new correct answer source object.",
        tags=["correct_answers_sources"]
    ),
    retrieve=extend_schema(
        summary="Retrieve a correct answer source",
        description="Retrieve a single correct answer source by its ID.",
        tags=["correct_answers_sources"]
    ),
    destroy=extend_schema(
        summary="Delete a correct answer source",
        description="Delete a correct answer source object by its ID.",
        tags=["correct_answers_sources"]
    ),
    update=extend_schema(
        summary="Update a correct answer source",
        description="Update all fields of a correct answer source object.",
        tags=["correct_answers_sources"]
    ),
    partial_update=extend_schema(
        summary="Partially update a correct answer source",
        description="Update some fields of a correct answer source object.",
        tags=["correct_answers_sources"]
    ),
)
class CorrectAnswersSourcesViewSet(ModelViewSet):
    serializer_class = CorrectAnswersSourcesSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_id")
        if question_id:
            return CorrectAnswersSources.objects.filter(alternative__question_id=question_id)
        return CorrectAnswersSources.objects.none()

    def get_permissions(self): 
        permission_classes = [IsAuthenticated, IsAdminUser] if self.action in ("create", "destroy", "update", "partial_update") else [IsAuthenticated]
        return [permission() for permission in permission_classes]
