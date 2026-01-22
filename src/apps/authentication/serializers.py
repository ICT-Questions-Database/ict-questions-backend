from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    EmailField,
    CharField,
    ValidationError,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from apps.users.models import User
from utils.validators import validate_unique_email


class UserRegistrationSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)
    email = EmailField(validators=[validate_unique_email])

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "password",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise ValidationError(
                detail="Credenciais inválidas.",
                code="invalid"
            )
        
        if not user.is_active:
            raise ValidationError(
                detail="Conta inativa ou não verificada.",
                code="invalid"
            )
        
        attrs["user"] = user
        return attrs
    

class UserLogoutSerializer(Serializer):
    refresh_token = CharField(required=True)

    def validate_refresh_token(self, value):
        try:
            RefreshToken(value)
        except Exception:
            raise ValidationError("Token inválido.")

        return value
