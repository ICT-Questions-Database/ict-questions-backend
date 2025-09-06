from django.urls import path
from .views import ExamAttemptViewSet, ExamQuestionViewSet

urlpatterns = [
    # ExamAttempt
    path("exam_attempts/", ExamAttemptViewSet.as_view({"get": "list"})),
    path("exam_attempts/<int:pk>/", ExamAttemptViewSet.as_view({"get": "retrieve"})),
    path("exam_attempts/start_exam/", ExamAttemptViewSet.as_view({"post": "start_exam"})),
    path("exam_attempts/<int:pk>/finish_exam/", ExamAttemptViewSet.as_view({"patch": "finish_exam"})),

    # ExamQuestion
    path("exam_questions/", ExamQuestionViewSet.as_view({"get": "list", "post": "create"})),
    path("exam_questions/<int:pk>/", ExamQuestionViewSet.as_view({"get": "retrieve"})),
]
