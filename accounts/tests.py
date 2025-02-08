# 예: accounts/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_register(self):
        response = self.client.post("/api/accounts/register/", {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpass"
        }, format="json")
        self.assertEqual(response.status_code, 201)

    def test_jwt_token_obtain(self):
        response = self.client.post("/api/token/", {
            "username": "testuser",
            "password": "testpass"
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
