from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserLogoutSerializer
from .schemas import register_schema, login_schema, logout_schema
from apps.users.serializers import UserSerializer


@register_schema
class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": _(
                    "Conta criada com sucesso. Aguarde pela ativação."
                ),
                "data": serializer.data,
            },
            status=201,
        )
    

@login_schema
class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "message": _("Login realizado com sucesso."),
                "data": UserSerializer(user).data,
                "tokens": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
            },
            status=200,
        )
    

@logout_schema
class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {"message": "Logout realizado com sucesso."},
            status=200
        )
