from django.urls import path
from .views import QuestionViewSet

urlpatterns = [
    path("", QuestionViewSet.as_view({"post": "create", "get": "list"})),
    path("<int:pk>/", QuestionViewSet.as_view({"delete": "destroy", "put": "update", "patch": "partial_update"})),
]
