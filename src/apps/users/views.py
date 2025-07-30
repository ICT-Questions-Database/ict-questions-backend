from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all().order_by("-id")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "put", "patch", "delete"]

    # Retorna o usuário autenticado
    def get_object(self):
        return self.request.user
