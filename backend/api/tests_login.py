import jwt
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from api.fixtures import TEST_PRIVATE_KEY, TEST_PUBLIC_KEY


@override_settings(JWT_PRIVATE_KEY=TEST_PRIVATE_KEY, JWT_PUBLIC_KEY=TEST_PUBLIC_KEY)
class LoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user(username='alice', password='correct-password')

    def test_returns_token_on_valid_credentials(self):
        response = self.client.post('/api/login/', {'username': 'alice', 'password': 'correct-password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_token_contains_correct_subject(self):
        response = self.client.post('/api/login/', {'username': 'alice', 'password': 'correct-password'})
        payload = jwt.decode(response.data['token'], TEST_PUBLIC_KEY, algorithms=['RS256'])
        self.assertEqual(payload['sub'], 'alice')

    def test_rejects_wrong_password(self):
        response = self.client.post('/api/login/', {'username': 'alice', 'password': 'wrong-password'})
        self.assertEqual(response.status_code, 401)

    def test_rejects_unknown_username(self):
        response = self.client.post('/api/login/', {'username': 'nobody', 'password': 'whatever'})
        self.assertEqual(response.status_code, 401)

    def test_rejects_missing_username(self):
        response = self.client.post('/api/login/', {'password': 'correct-password'})
        self.assertEqual(response.status_code, 400)

    def test_rejects_missing_password(self):
        response = self.client.post('/api/login/', {'username': 'alice'})
        self.assertEqual(response.status_code, 400)
