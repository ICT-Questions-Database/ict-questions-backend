from django.urls import path
from .views import QuestionViewSet, AlternativeViewSet, CorrectAnswersSourcesViewSet

urlpatterns = [
    path("", QuestionViewSet.as_view({"post": "create", "get": "list"})),
    path("<int:pk>/", QuestionViewSet.as_view({"delete": "destroy", "put": "update", "patch": "partial_update"})),

    path("alternatives/", AlternativeViewSet.as_view({"get": "list", "post": "create"})),
    path("alternatives/<int:pk>/", AlternativeViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update", "patch": "partial_update"})),

    path("correct_answers_sources/", CorrectAnswersSourcesViewSet.as_view({"get": "list", "post": "create"})),
    path("correct_answers_sources/<int:pk>/", CorrectAnswersSourcesViewSet.as_view({"get": "retrieve", "delete": "destroy", "put": "update", "patch": "partial_update"}))
]
