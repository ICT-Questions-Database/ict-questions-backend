from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import QuestionSubmission
from .serializers import QuestionSubmissionSerializer
from .permissions import IsAdminOrOwner
from .services import review_submission
from .pagination import SubmissionPagination

class QuestionSubmissionViewset(ModelViewSet):
    serializer_class = QuestionSubmissionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    pagination_class = SubmissionPagination
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return QuestionSubmission.objects.all()
        return QuestionSubmission.objects.filter(submitted_by=user)
    
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
