from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterViewSet, UserProfileViewSet, MyTokenObtainPairView

urlpatterns = [
    # JWT
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Registro
    path("register/", UserRegisterViewSet.as_view({"post": "create"})),

    # Perfil
    path(
        "me/",
        UserProfileViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),

    # Mudança de senha
    path("me/change_password/", UserProfileViewSet.as_view({"post": "change_password"})),
]
