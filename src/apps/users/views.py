from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import CustomUser
from .serializers import (
    StudentUserSerializer,
    MyTokenObtainPairSerializer,
)


@extend_schema_view(
    create=extend_schema(
        summary="Creates a user object",
        description="Creates a new user object.",
    ),
)
class UserRegisterViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [AllowAny]  # não precisa estar autenticado para registrar
    http_method_names = ["post"]


@extend_schema_view(
    change_password=extend_schema(
        summary="Changes user password",
        description="Changes a user object password.",
    ),
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
    queryset = CustomUser.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [IsAuthenticated]  # precisa estar autenticado para acessar
    http_method_names = ["get", "post", "put", "patch", "delete"]

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        user = self.get_object()
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response(
                {"detail": "Both current_password and new_password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password updated successfully"})
    
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
