from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import ExamAttempt, ExamQuestion
from .serializers import ExamAttemptSerializer, ExamQuestionSerializer

class ExamAttemptViewSet(ModelViewSet):
    serializer_class = ExamAttemptSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

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
        """
        Marca o exame como finalizado, calcula end_date e duration, e atualiza a nota
        """
        attempt = self.get_object()

        # Atualiza a nota 
        attempt.grade = request.data.get("grade", attempt.grade)

        # Marca fim e calcula duração
        attempt.finish()

        serializer = self.get_serializer(attempt)
        return Response(serializer.data)


class ExamQuestionViewSet(ModelViewSet):
    queryset = ExamQuestion.objects.all()
    serializer_class = ExamQuestionSerializer
    permission_classes = [IsAdminUser]
    http_method_names = ["get", "post"]