from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from apps.users.models import CustomUser


class AuthTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

        self.register_url = reverse("user_register")
        self.login_url = reverse("token_obtain_pair")
        self.refresh_url = reverse("token_refresh")

    # ---------- Register ----------
    def test_register_user_success(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
            "first_name": "New",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_register_user_missing_fields(self):
        data = {"username": "incomplete"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_duplicate_email(self):
        data = {
            "username": "dupuser",
            "email": "test@example.com", 
            "password": "passworddup",
            "first_name": "Dup",
            "last_name": "User",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Login ----------
    def test_login_user_success(self):
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "password123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_password(self):
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_nonexistent_user(self):
        response = self.client.post(
            self.login_url,
            {"email": "ghost@example.com", "password": "irrelevant"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_missing_fields(self):
        response = self.client.post(self.login_url, {"email": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ---------- Refresh ----------
    def test_refresh_token_success(self):
        login = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "password123"},
            format="json",
        )
        refresh = login.data["refresh"]

        response = self.client.post(self.refresh_url, {"refresh": refresh}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_refresh_token_invalid(self):
        response = self.client.post(self.refresh_url, {"refresh": "invalid"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_missing(self):
        response = self.client.post(self.refresh_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
