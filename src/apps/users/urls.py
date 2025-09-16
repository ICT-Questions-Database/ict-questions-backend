from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterViewSet, UserProfileViewSet, UserActionsViewSet, MyTokenObtainPairView

urlpatterns = [
    # JWT
    path("auth/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

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
    path("change_password/", UserActionsViewSet.as_view({"post": "change_password"})),
]
