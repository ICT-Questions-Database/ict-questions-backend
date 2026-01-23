from apps.questions.serializers import QuestionSerializer, AlternativeSerializer, CorrectAnswersSourcesSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .models import Question, Alternative, CorrectAnswersSources
from .pagination import QuestionsPagination
from .permissions import IsAdminOrReadOnly
from .filters import QuestionFilter

from .schema import question_schema, alternative_schema, correct_answers_sources_schema
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser



@question_schema
class QuestionViewSet(ModelViewSet):
    queryset = Question.objects.all().order_by("id")
    serializer_class = QuestionSerializer
    # permission_classes = [IsAdminOrReadOnly]
    pagination_class = QuestionsPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = QuestionFilter
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            reviewed_by=user if user.is_authenticated else None
        )


@alternative_schema
class AlternativeViewSet(ModelViewSet):
    serializer_class = AlternativeSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ["post", "put", "delete", "patch"]
 
    queryset = Alternative.objects.all()
 
    # def get_permissions(self):
    #     permission_classes = [IsAuthenticated, IsAdminUser] if self.action in ("create", "destroy", "update", "partial_update") else [IsAuthenticated]
    #     return [permission() for permission in permission_classes]


@correct_answers_sources_schema
class CorrectAnswersSourcesViewSet(ModelViewSet):
    serializer_class = CorrectAnswersSourcesSerializer
    # permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "delete", "patch"]

    def get_queryset(self):
        question_id = self.request.query_params.get("question_id")
        if question_id:
            return CorrectAnswersSources.objects.filter(alternative__question_id=question_id)
        return CorrectAnswersSources.objects.none()

    def get_permissions(self): 
        permission_classes = [IsAuthenticated, IsAdminUser] if self.action in ("create", "destroy", "update", "partial_update") else [IsAuthenticated]
        return [permission() for permission in permission_classes]
