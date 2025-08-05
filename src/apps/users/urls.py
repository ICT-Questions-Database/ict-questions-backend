from django.urls import path
from .views import UserRegisterViewSet, UserProfileViewSet, MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

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
