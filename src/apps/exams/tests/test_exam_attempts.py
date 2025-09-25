from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from apps.exams.models import ExamAttempt


User = get_user_model()


class ExamAttemptAPITestCase(APITestCase):
    def setUp(self):
        # cria usuário de teste
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass"
        )

        # gera token JWT para autenticação
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_start_exam(self):
        url = reverse("examattempt-start-exam")  # /api/v1/exams/exam_attempts/start_exam/
        payload = {"track": "cloud", "level": "hcia"}

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["track"], "cloud")
        self.assertEqual(response.data["level"], "hcia")
        self.assertEqual(ExamAttempt.objects.count(), 1)

    def test_finish_exam(self):
        attempt = ExamAttempt.objects.create(
            user=self.user, track="cloud", level="hcia", grade=0.0
        )
        url = reverse("examattempt-finish-exam", kwargs={"pk": attempt.id})
        payload = {"grade": 8.5}

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        attempt.refresh_from_db()
        self.assertEqual(attempt.grade, 8.5)
        self.assertIsNotNone(attempt.end_date)
        self.assertIsNotNone(attempt.duration)

    def test_list_attempts_only_user(self):
        # tentativa do usuário autenticado
        ExamAttempt.objects.create(
            user=self.user, track="cloud", level="hcia", grade=5.0
        )

        # tentativa de outro usuário
        other = User.objects.create_user(
            username="other",
            email="other@example.com",
            password="otherpass"
        )
        ExamAttempt.objects.create(
            user=other, track="network", level="hcip", grade=7.0
        )

        url = reverse("examattempt-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["track"], "cloud")
