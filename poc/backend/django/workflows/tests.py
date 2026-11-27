from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Workflow

User = get_user_model()


class WorkflowAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!",
        )
        self.client.force_authenticate(user=self.user)

    def test_create_and_list_workflow(self):
        response = self.client.post(
            "/api/workflows",
            {"name": "My workflow"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/workflows")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_toggle_workflow(self):
        workflow = Workflow.objects.create(
            owner=self.user,
            name="My workflow",
        )
        response = self.client.patch(
            f"/api/workflows/{workflow.id}/enabled",
            {"enabled": False},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        workflow.refresh_from_db()
        self.assertFalse(workflow.enabled)

    def test_register_and_login(self):
        response = self.client.post(
            "/api/auth/register",
            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "AnotherPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

        self.client.force_authenticate(user=None)
        response = self.client.post(
            "/api/auth/login",
            {
                "username": "newuser",
                "password": "AnotherPassword123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_workflows_require_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/workflows")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
