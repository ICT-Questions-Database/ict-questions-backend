from django.urls import path
from .views import ExamAttemptViewSet, ExamQuestionViewSet

urlpatterns = [
    # ExamAttempt
    path("exam_attempts/", ExamAttemptViewSet.as_view({"get": "list"})),
    path("exam_attempts/{id}/", ExamAttemptViewSet.as_view({"get": "retrieve"})),
    path("exam_attempts/start_exam/", ExamAttemptViewSet.as_view({"post": "start_exam"})),
    path("exam_attempts/{id}/finish_exam/", ExamAttemptViewSet.as_view({"patch": "finish_exam"})),

    # ExamQuestion
    path("exam_question/", ExamQuestionViewSet.as_view({"get": "list", "post": "create"})),
    path("exam_question/{id}/", ExamQuestionViewSet.as_view({"get": "retrieve"})),
]
