from django.urls import path
from .views import QuestionSubmissionViewset, CorrectSubmissionAnswersSourcesViewSet

urlpatterns = [
    path(
        "question_submissions/",
        QuestionSubmissionViewset.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "question_submissions/<int:pk>/",
        QuestionSubmissionViewset.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "question_submissions/review/<int:pk>/",
        QuestionSubmissionViewset.as_view(
            {
                "patch": "review",
            }
        ),
    ),
    path(
        "correct_submission_answers_sources/",
        CorrectSubmissionAnswersSourcesViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
    ),
    path(
        "correct_submission_answers_sources/<int:pk>/",
        CorrectSubmissionAnswersSourcesViewSet.as_view(
            {
                "put": "update",
                "delete": "destroy",
            }
        ),
    ),
]
