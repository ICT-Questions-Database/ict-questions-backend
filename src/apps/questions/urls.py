from django.urls import path
from .views import QuestionViewSet

urlpatterns = [
    path("create/", QuestionViewSet.as_view({"post": "create"})),
]
