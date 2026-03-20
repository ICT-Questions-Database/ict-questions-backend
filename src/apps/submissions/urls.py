from rest_framework.routers import DefaultRouter
from .views import (
    QuestionSubmissionViewset,
    CorrectSubmissionAnswersSourcesViewSet,
    AlternativeSubmissionViewSet,
)

router = DefaultRouter()

router.register(
    r"question-submissions",
    QuestionSubmissionViewset,
    basename="question-submission"
)

router.register(
    r"correct-submission-answer-sources",
    CorrectSubmissionAnswersSourcesViewSet,
    basename="correct-submission-answer-sources"
)

router.register(
    r"alternative-submissions",
    AlternativeSubmissionViewSet,
    basename="alternative-submission"
)

urlpatterns = router.urls
