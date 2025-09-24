from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.users.models import CustomUser


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

        # URLs usando reverse
        self.login_url = reverse("token_obtain_pair")       # /api/v1/users/auth/token/
        self.profile_url = reverse("user_profile")          # /api/v1/users/me/
        self.change_password_url = reverse("change_password")  # /api/v1/users/change_password/

    def authenticate(self):
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "password123"},
            format="json",
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # ---------- Perfil ----------
    def test_get_profile(self):
        self.authenticate()
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_update_profile(self):
        self.authenticate()
        response = self.client.patch(
            self.profile_url, {"first_name": "Changed"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Changed")

    def test_update_profile_invalid_email(self):
        self.authenticate()
        # Criar outro usuário com o mesmo email que vamos tentar usar
        CustomUser.objects.create_user(
            username="otheruser",
            email="other@example.com",
            password="password456"
        )
        # Tentar atualizar para o email do outro usuário
        response = self.client.patch(self.profile_url, {"email": "other@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account_with_wrong_password(self):
        self.authenticate()
        response = self.client.delete(
            self.profile_url, {"password": "wrongpass"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_account_success(self):
        self.authenticate()
        response = self.client.delete(self.profile_url, {"password": "password123"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.filter(email="test@example.com").count(), 0)

    # ---------- Mudança de senha ----------
    def test_change_password_success(self):
        self.authenticate()
        response = self.client.post(
            self.change_password_url,
            {"current_password": "password123", "new_password": "newpass456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Confirmar login com nova senha
        login = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "newpass456"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_current(self):
        self.authenticate()
        response = self.client.post(
            self.change_password_url,
            {"current_password": "wrongpass", "new_password": "newpass456"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_password_missing_fields(self):
        self.authenticate()
        response = self.client.post(self.change_password_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
