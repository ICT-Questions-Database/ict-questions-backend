from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('api/v1/auth/', include("apps.users.urls")),
]
