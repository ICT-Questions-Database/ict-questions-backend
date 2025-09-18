from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.questions.models import Question

User = get_user_model()

class QuestionViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="student", email="student@example.com", password="pass123")
        self.staff = User.objects.create_user(username="admin", email="admin@example.com", password="pass123", is_staff=True)
        self.url = "/api/v1/questions/"

        self.payload = {
            "text": "New Q",
            "level": "HCIA",
            "has_answer": False,
            "has_multiple_answers": False,
            "track": "Network",
            "weight": 1.0
        }

        self.question = Question.objects.create(
            text="What is 2+2?",
            submitted_by=self.user,
            reviewed_by=self.staff,
            level=Question.Level.HCIA,
            track=Question.Track.COMPUTING,
            has_answer=False,
            has_multiple_answers=False,
            weight=1.0
        )
        self.detail_url = f"/api/v1/questions/{self.question.id}/"

    def auth_as(self, user):
        self.client.force_authenticate(user=user)

    def test_list_questions_requires_auth(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_questions_as_user(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()["results"]), 1)


    def test_non_staff_cannot_modify_question(self):
        self.auth_as(self.user)
        actions = {
            "POST": lambda: self.client.post(self.url, self.payload),
            "DELETE": lambda: self.client.delete(self.detail_url, self.payload),
            "PUT": lambda: self.client.put(self.detail_url, self.payload),
            "PATCH": lambda: self.client.patch(self.detail_url, self.payload)
        }

        for action, call in actions.items():
            with self.subTest(action=action):
                res = call()
                self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_crud_question(self):
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
