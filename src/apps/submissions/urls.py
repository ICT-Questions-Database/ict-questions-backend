from django.urls import path
from .views import QuestionSubmissionViewset

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
        )
    ),
]
