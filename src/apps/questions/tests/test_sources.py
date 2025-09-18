from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.questions.models import Question, Alternative, CorrectAnswersSources

User = get_user_model()


class CorrectAnswersSourcesViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        self.question = Question.objects.create(
            submitted_by=self.user,
            reviewed_by=self.user,
            text="What is 2+2",
            level=Question.Level.HCIA,
            has_answer=True,
            has_multiple_answers=False,
            track=Question.Track.CLOUD,
            weight=1.0,
        )

        self.alternative = Alternative.objects.create(
            question=self.question,
            text="Alt 1",
            is_correct=True
        )

        self.source = CorrectAnswersSources.objects.create(
            alternative=self.alternative,
            source="http://example.com"
        )

        self.list_url = "/api/v1/questions/correct_answers_sources/"
        self.detail_url = f"/api/v1/questions/correct_answers_sources/{self.source.id}/"

    def auth_as(self, user):
        self.client.force_authenticate(user=user)

    def test_requires_authentication_on_detail(self):
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_collection_not_allowed(self):
        self.auth_as(self.user)
        res = self.client.get(self.list_url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_source_not_allowed(self):
        self.auth_as(self.user)
        res = self.client.get(self.detail_url)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_non_staff_cannot_crud(self):
        self.auth_as(self.user)

        actions = {
            "DELETE": lambda: self.client.delete(self.detail_url),
            "PUT": lambda: self.client.put(self.detail_url, data={"source": "http://new.com"}),
            "PATCH": lambda: self.client.patch(self.detail_url, data={"source": "http://new.com"}),
        }

        for method, func in actions.items():
            with self.subTest(method=method):
                res = func()
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
