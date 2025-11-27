from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from fridge.models import Fridge, Item

class ItemCRUDTests(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.other_user = User.objects.create_user(username='otheruser', password='123456')

        # Create fridges
        self.fridge = Fridge.objects.create(name="My Fridge", owner=self.user)
        self.other_fridge = Fridge.objects.create(name="Other Fridge", owner=self.other_user)

        # Obtain JWT token
        response = self.client.post(reverse('login'), {
            "username": "testuser",
            "password": "123456"
        }, format='json')
        self.access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_item(self):
        url = reverse('item-list')
        data = {
            "fridge": self.fridge.id,
            "name": "Milk",
            "quantity": 2,
            "best_before": "2025-12-01"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, "Milk")

    def test_list_items(self):
        Item.objects.create(name="Milk", fridge=self.fridge)
        Item.objects.create(name="Eggs", fridge=self.fridge)
        Item.objects.create(name="Cheese", fridge=self.other_fridge)
        url = reverse('item-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_item(self):
        item = Item.objects.create(name="Milk", fridge=self.fridge)
        url = reverse('item-detail', args=[item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Milk")

    def test_update_item(self):
        item = Item.objects.create(name="Milk", fridge=self.fridge)
        url = reverse('item-detail', args=[item.id])
        data = {"name": "Soy Milk", "quantity": 3}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, "Soy Milk")
        self.assertEqual(item.quantity, 3)

    def test_partial_update_item(self):
        item = Item.objects.create(name="Milk", fridge=self.fridge)
        url = reverse('item-detail', args=[item.id])
        data = {"quantity": 5}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_delete_item(self):
        item = Item.objects.create(name="Milk", fridge=self.fridge)
        url = reverse('item-detail', args=[item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_user_cannot_access_others_items(self):
        item = Item.objects.create(name="Milk", fridge=self.other_fridge)
        url = reverse('item-detail', args=[item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_add_item_to_other_users_fridge(self):
        url = reverse('item-list')
        data = {"fridge": self.other_fridge.id, "name": "Milk"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
