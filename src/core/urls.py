from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Apps
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/questions/", include("apps.questions.urls")),
    path("api/v1/exams/", include("apps.exams.urls")),
    # Swagger
    path("api/v1/swagger/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),
]
