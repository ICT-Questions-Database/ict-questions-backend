from rest_framework.viewsets import ModelViewSet
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
    http_method_names = ["get", "put", "patch", "delete"]

    def get_object(self):
        return self.request.user


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
