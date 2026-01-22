from django.contrib import admin
from django.urls import path, include
from core import settings
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("docs/schema", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path(f"api/{settings.API_MAJOR}/users/", include("apps.users.urls")),
    path(f"api/{settings.API_MAJOR}/auth/", include("apps.authentication.urls")),
    path(f"api/{settings.API_MAJOR}/questions/", include("apps.questions.urls")),
    path(f"api/{settings.API_MAJOR}/exams/", include("apps.exams.urls")),
    path(f"api/{settings.API_MAJOR}/submissions/", include("apps.submissions.urls")),
]
