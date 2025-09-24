from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import CustomUser
from apps.exams.models import ExamAttempt
from apps.questions.models import Question, Alternative
from django.urls import reverse


class UserAnswersTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
        )

        self.login_url = reverse("token_obtain_pair")
        self.user_answers_url = reverse("user_answers")

    def authenticate(self):
        response = self.client.post(
            self.login_url,
            {"email": "test@example.com", "password": "password123"},
            format="json",
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # ---------- Criação e listagem ----------
    def test_create_and_list_user_answer_success(self):
        self.authenticate()

        exam_attempt = ExamAttempt.objects.create(
            user=self.user,
            grade=0.0,
            track="cloud",
            level="hcia",
        )

        question = Question.objects.create(
            text="Pergunta teste?",
            has_answer=True,
            has_multiple_answers=False,
            level="HCIA",
            track="Cloud",
            weight=1.0
        )

        alternative = Alternative.objects.create(
            question=question,
            text="Opção 1",
            is_correct=True
        )

        data = {
            "user": self.user.id,
            "exam_attempt": exam_attempt.id,
            "question": question.id,
            "alternative": alternative.id,
        }

        response = self.client.post(self.user_answers_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Listagem
        response = self.client.get(f"{self.user_answers_url}?exam_attempt={exam_attempt.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_user_answer_unauthenticated(self):
        exam_attempt = ExamAttempt.objects.create(user=self.user, grade=0.0, track="cloud", level="hcia")
        question = Question.objects.create(text="Pergunta?", has_answer=True, has_multiple_answers=False, level="HCIA", track="Cloud", weight=1)
        alternative = Alternative.objects.create(question=question, text="Alt", is_correct=True)

        data = {"user": self.user.id, "exam_attempt": exam_attempt.id, "question": question.id, "alternative": alternative.id}
        response = self.client.post(self.user_answers_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_answer_invalid_data(self):
        self.authenticate()
        response = self.client.post(self.user_answers_url, {"user": 999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user_answers_unauthenticated(self):
        response = self.client.get(self.user_answers_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
