from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from fridge.models import Fridge

class FridgeCRUDTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123456')

        response = self.client.post(reverse('login'), {
            "username": "testuser",
            "password": "123456"
        }, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_fridge(self):
        url = reverse('fridge-list')
        data = {"name": "Kitchen Fridge", "description": "For snacks"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Fridge.objects.count(), 1)
        self.assertEqual(Fridge.objects.get().name, "Kitchen Fridge")

    def test_list_fridges(self):
        Fridge.objects.create(name="Fridge1", owner=self.user)
        Fridge.objects.create(name="Fridge2", owner=self.user)
        url = reverse('fridge-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_fridge(self):
        fridge = Fridge.objects.create(name="Fridge1", owner=self.user)
        url = reverse('fridge-detail', args=[fridge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Fridge1")

    def test_update_fridge(self):
        fridge = Fridge.objects.create(name="Old Name", owner=self.user)
        url = reverse('fridge-detail', args=[fridge.id])
        data = {"name": "New Name", "description": "Updated"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fridge.refresh_from_db()
        self.assertEqual(fridge.name, "New Name")
        self.assertEqual(fridge.description, "Updated")

    def test_partial_update_fridge(self):
        fridge = Fridge.objects.create(name="Old Name", owner=self.user)
        url = reverse('fridge-detail', args=[fridge.id])
        data = {"description": "Partial update"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        fridge.refresh_from_db()
        self.assertEqual(fridge.description, "Partial update")

    def test_delete_fridge(self):
        fridge = Fridge.objects.create(name="To Delete", owner=self.user)
        url = reverse('fridge-detail', args=[fridge.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Fridge.objects.count(), 0)

    def test_user_cannot_access_others_fridge(self):
        other_user = User.objects.create_user(username='other', password='123456')
        fridge = Fridge.objects.create(name="Other Fridge", owner=other_user)
        url = reverse('fridge-detail', args=[fridge.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
