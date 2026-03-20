from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.questions.models import Question, Alternative

User = get_user_model()

class AlternativeViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="student", email="student@example.com", password="pass123"
        )
        self.staff = User.objects.create_user(
            username="admin", email="admin@example.com", password="pass123", is_staff=True
        )

        self.question = Question.objects.create(
            text="What is 2+2?",
            submitted_by=self.user,
            reviewed_by=self.staff,
            level=Question.Level.HCIA,
            track=Question.Track.COMPUTING,
            has_answer=True,
            has_multiple_answers=False,
            weight=1.0,
        )

        self.alternative = Alternative.objects.create(
            question=self.question,
            text="4",
            is_correct=True,
        )

        self.url = "/api/v1/questions/alternatives/"
        self.detail_url = f"/api/v1/questions/alternatives/{self.alternative.id}/"

        self.payload = {
            "question": self.question.id,
            "text": "3",
            "is_correct": False,
        }

    def test_list_alternatives_as_user(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_non_staff_cannot_crud_alternatives(self):
        self.client.force_authenticate(user=self.user)

        actions = {
            "POST": lambda: self.client.post(self.url, self.payload),
            "PUT": lambda: self.client.put(self.detail_url, self.payload),
            "PATCH": lambda: self.client.patch(self.detail_url, {"text": "patched"}),
            "DELETE": lambda: self.client.delete(self.detail_url),
        }

        for action, call in actions.items():
            with self.subTest(action=action):
                res = call()
                self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_crud_alternatives(self):
        self.client.force_authenticate(user=self.staff)

        actions = {
            "POST": (lambda: self.client.post(self.url, self.payload), status.HTTP_201_CREATED),
            "PUT": (lambda: self.client.put(self.detail_url, self.payload), status.HTTP_200_OK),
            "PATCH": (lambda: self.client.patch(self.detail_url, {"text": "patched"}), status.HTTP_200_OK),
            "DELETE": (lambda: self.client.delete(self.detail_url), status.HTTP_204_NO_CONTENT),
        }

        for action, (call, expected_status) in actions.items():
            with self.subTest(action=action):
                res = call()
                self.assertEqual(res.status_code, expected_status)
