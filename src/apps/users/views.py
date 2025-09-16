from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import CustomUser
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    MyTokenObtainPairSerializer,
)
from .services import delete_user_account, change_user_password
from .exceptions import MissingPasswordError, InvalidPasswordError


@extend_schema_view(
    create=extend_schema(
        summary="Creates a user object",
        description="Creates a new user object.",
    ),
)
class UserRegisterViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]


@extend_schema_view(
    retrieve=extend_schema(
        summary="Retrieve a user's personal information",
        description="Returns a user's personal information.",
    ),
    update=extend_schema(
        summary="Updates a user personal information",
        description="Updates a user personal information.",
    ),
    partial_update=extend_schema(
        summary="Partially updates a user personal information",
        description="Partially updates a user personal information.",
    ),
    destroy=extend_schema(
        summary="Deletes a user",
        description="Deletes a user.",
    ),
)
class UserProfileViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "patch", "delete"]

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        password = request.data.get("password")

        try:
            delete_user_account(user=user, password=password)
            return Response(
                {"detail": "Account deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except MissingPasswordError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidPasswordError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )


@extend_schema_view(
    change_password=extend_schema(
        summary="Changes user password",
        description="Changes authenticated user password.",
    ),
)
class UserActionsViewSet(ModelViewSet):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["post"]

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        serializer_class=ChangePasswordSerializer,
    )
    def change_password(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        try:
            change_user_password(user, current_password, new_password)
            return Response(
                {"detail": "Password changed successfully."},
                status=status.HTTP_200_OK,
            )
        except MissingPasswordError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidPasswordError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
