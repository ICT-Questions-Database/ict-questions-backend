from django.urls import path
from rest_framework import routers
from .views import (
    UserViewSet
)

router = routers.DefaultRouter()

urlpatterns = [
    path("me/", UserViewSet.as_view()),
] + router.urls