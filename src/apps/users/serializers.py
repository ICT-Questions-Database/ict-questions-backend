from rest_framework.serializers import ModelSerializer, Serializer, EmailField, CharField, ValidationError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import CustomUser, UserAnswers


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "created_at"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        user = self.instance
        if user and CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise ValidationError("Este email já está em uso.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(Serializer):
    current_password = CharField(write_only=True, required=True)
    new_password = CharField(write_only=True, required=True)


class UserAnswersSerializer(ModelSerializer):
    class Meta:
        model = UserAnswers
        fields = "__all__"


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = EmailField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(username=email, password=password)

        if not user:
            raise AuthenticationFailed("No active account found with the given credentials")

        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return data
