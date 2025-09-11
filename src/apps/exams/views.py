from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ExamAttempt, ExamQuestion
from .serializers import ExamAttemptSerializer, ExamQuestionSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from .services import finish_exam_attempt


@extend_schema_view(
    list=extend_schema(
        summary="Lists all authenticated user questions",
        description="Lists all authenticated user questions at once.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific question",
        description="Retrieve a specific question from the authenticated user.",
    ),
    start_exam=extend_schema(
        summary="Creates an exam instance",
        description="Creates an exam instance to be completed.",
    ),
    finish_exam=extend_schema(
        summary="Updates an exam instance",
        description="Updates an exam instance filling the incomplete data.",
    ),
)
class ExamAttemptViewSet(ModelViewSet):
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        # Retorna apenas as tentativas do usuário logado
        return ExamAttempt.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def start_exam(self, request):
        """
        Cria um ExamAttempt quando o usuário inicia a prova
        """
        track = request.data.get("track")
        level = request.data.get("level")

        attempt = ExamAttempt.objects.create(
            user=request.user,
            track=track,
            level=level,
            grade=0.0  
        )
        serializer = self.get_serializer(attempt)
        return Response(serializer.data)
    
    @action(detail=True, methods=["patch"])
    def finish_exam(self, request, pk=None):
        attempt = self.get_object()
        grade = request.data.get("grade")

        attempt = finish_exam_attempt(attempt, grade)
        serializer = self.get_serializer(attempt)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        summary="Lists all authenticated user questions",
        description="Lists all authenticated user questions at once.",
    ),
    retrieve=extend_schema(
        summary="Retrieve a specific question",
        description="Retrieve a specific question from the authenticated user.",
    ),
    create=extend_schema(
        summary="Creates an exam_question object",
        description="Creates an exam_question object."
    )
)
class ExamQuestionViewSet(ModelViewSet):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post"]