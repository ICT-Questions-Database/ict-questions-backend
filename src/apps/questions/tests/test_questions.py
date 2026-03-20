from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.questions.models import Question

User = get_user_model()


class QuestionViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="student", email="student@example.com", password="pass123"
        )
        self.staff = User.objects.create_user(
            username="admin", email="admin@example.com", password="pass123", is_staff=True
        )
        self.url = "/api/v1/questions/"

        self.payload = {
            "text": "New Q",
            "level": "HCIA",
            "has_answer": False,
            "has_multiple_answers": False,
            "track": "Network",
            "weight": 1.0,
        }

        self.question = Question.objects.create(
            text="What is 2+2?",
            submitted_by=self.user,
            reviewed_by=self.staff,
            level=Question.Level.HCIA,
            track=Question.Track.COMPUTING,
            has_answer=False,
            has_multiple_answers=False,
            weight=1.0,
        )
        self.detail_url = f"/api/v1/questions/{self.question.id}/"

    def auth_as(self, user):
        self.client.force_authenticate(user=user)

    def test_list_questions_requires_auth(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_questions_as_user(self):
        self.auth_as(user=self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.json()["results"]), 1)

    def test_retrieve_question(self):
        self.auth_as(self.user)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_computing_questions(self):
        self.auth_as(self.user)
        res = self.client.get(self.url, {"track": "Computing"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(data["results"][0]["track"], "Computing")

    def test_filter_by_level(self):
        self.auth_as(self.user)
        res = self.client.get(self.url, {"level": "HCIA"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertTrue(all(q["level"] == "HCIA" for q in data["results"]))

    def test_filter_by_text(self):
        self.auth_as(self.user)
        res = self.client.get(self.url, {"text": "2+2"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(len(data["results"]), 1)
        self.assertIn("2+2", data["results"][0]["text"])

    def test_filter_returns_empty(self):
        self.auth_as(self.user)
        res = self.client.get(self.url, {"track": "Cloud"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.json()
        self.assertEqual(len(data["results"]), 0)

    def test_non_staff_cannot_modify_question(self):
        self.auth_as(self.user)
        actions = {
            "POST": lambda: self.client.post(self.url, self.payload),
            "DELETE": lambda: self.client.delete(self.detail_url),
            "PUT": lambda: self.client.put(self.detail_url, self.payload),
            "PATCH": lambda: self.client.patch(self.detail_url, self.payload),
        }

        for action, call in actions.items():
            with self.subTest(action=action):
                res = call()
                self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_crud_question(self):
        self.auth_as(self.staff)

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
