from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserRegisterViewSet, UserProfileViewSet, UserActionsViewSet, UserAnswersViewSet, MyTokenObtainPairView

urlpatterns = [
    # JWT
    path("auth/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Registro
    path("register/", UserRegisterViewSet.as_view({"post": "create"}), name="user_register"),

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
        ), name="user_profile"
    ),

    # Mudança de senha
    path("change_password/", UserActionsViewSet.as_view({"post": "change_password"}), name="change_password"),
    
    # UserAnswers
    path("user_answers/", UserAnswersViewSet.as_view({"get": "list", "post": "create"}), name="user_answers"),
]
