from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User


class RegistrationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456')

    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "milan",
            "email": "milan@example.com",
            "password": "pass123",
            "password2": "pass123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='milan').exists())

    def test_password_mismatch(self):
        url = reverse('register')
        data = {
            "username": "bob",
            "email": "bob@example.com",
            "password": "pass1",
            "password2": "pass2"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_login_user(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "123456"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_user_wrong_pass(self):
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "1234567"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
