from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import (
    UserSerializer,
    ChangePasswordSerializer,
    UserAnswersSerializer,
    MyTokenObtainPairSerializer,
)
from .services import (
    delete_user_account,
    change_user_password,
    get_user_answers_by_exam,
)
from .exceptions import MissingPasswordError, InvalidPasswordError
from .schema import (
    user_register_schema,
    user_profile_schema,
    user_actions_schema,
    user_answers_schema,
)


@user_register_schema
class UserRegisterViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ["post"]


@user_profile_schema
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


@user_actions_schema
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


@user_answers_schema
class UserAnswersViewSet(ModelViewSet):
    serializer_class = UserAnswersSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        user = self.request.user
        exam_attempt_id = self.request.query_params.get("exam_attempt")

        queryset = get_user_answers_by_exam(user=user, exam_attempt_id=exam_attempt_id)
        return queryset


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
