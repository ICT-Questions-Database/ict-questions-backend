from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser
from .serializers import (
    StudentUserSerializer,
    MyTokenObtainPairSerializer,
)


class UserRegisterViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = StudentUserSerializer
    permission_classes = [AllowAny]  # não precisa estar autenticado para registrar
    http_method_names = ["post"]


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
