from django.urls import path
from .views import ExamAttemptViewSet, ExamQuestionViewSet

urlpatterns = [
    # ExamAttempt
    path("exam_attempts/", ExamAttemptViewSet.as_view({"get": "list"}), name="examattempt-list"),
    path("exam_attempts/<int:pk>/", ExamAttemptViewSet.as_view({"get": "retrieve"}), name="examattempt-detail"),
    path("exam_attempts/start_exam/", ExamAttemptViewSet.as_view({"post": "start_exam"}), name="examattempt-start-exam"),
    path("exam_attempts/<int:pk>/finish_exam/", ExamAttemptViewSet.as_view({"patch": "finish_exam"}), name="examattempt-finish-exam"),

    # ExamQuestion
    path("exam_questions/", ExamQuestionViewSet.as_view({"get": "list", "post": "create"}), name="examquestion-list"),
    path("exam_questions/<int:pk>/", ExamQuestionViewSet.as_view({"get": "retrieve"}), name="examquestion-detail"),
]
