from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from apps.exams.models import ExamAttempt, ExamQuestion
from apps.questions.models import Question

User = get_user_model()


class ExamQuestionAPITestCase(APITestCase):
    def setUp(self):
        # Cria usuário comum
        self.user = User.objects.create_user(
            username="normal",
            email="normal@example.com",
            password="123456",
            is_staff=False,
            first_name="Normal",
            last_name="User"
        )

        # Cria usuário admin
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="123456",
            is_staff=True,
            first_name="Admin",
            last_name="User"
        )

        # Autentica o client como usuário comum
        self.client.force_authenticate(user=self.user)

    def authenticate_as_admin(self):
        # Troca o usuário autenticado para admin
        self.client.force_authenticate(user=self.admin)

    def create_question(self):
        return Question.objects.create(
            text="Pergunta teste",
            level="HCIA",
            has_answer=True,
            has_multiple_answers=False,
            track="Cloud",
            weight=1.0,
            submitted_by=self.user,
        )

    def create_attempt(self):
        return ExamAttempt.objects.create(
            user=self.user,
            grade=0.0,
            track="cloud",
            level="hcia",
        )

    def test_exam_question_requires_admin(self):
        q = self.create_question()
        attempt = self.create_attempt()

        url = reverse("examquestion-list")
        payload = {"exam_attempt": attempt.id, "question": q.id}

        # Usuário comum não pode criar
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Autentica como admin
        self.authenticate_as_admin()
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExamQuestion.objects.count(), 1)

    def test_list_exam_questions_admin_only(self):
        q = self.create_question()
        attempt = self.create_attempt()
        ExamQuestion.objects.create(exam_attempt=attempt, question=q)

        url = reverse("examquestion-list")

        # Usuário comum não pode listar
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin pode listar
        self.authenticate_as_admin()
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
