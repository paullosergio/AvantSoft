from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer

from .models import Sale


class SaleAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.customer = Customer.objects.create(name="Cliente Teste", email="cliente@example.com")
        self.url = reverse("sales-list")
        self.sale_data = {"customer": self.customer.id, "amount": "100.00", "date": "2024-06-01"}

    def authenticate(self):
        response = self.client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_auth_required(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_sale(self):
        self.authenticate()
        response = self.client.post(self.url, self.sale_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 1)
        self.assertEqual(Sale.objects.get().amount, 100.00)

    def test_stats_daily(self):
        self.authenticate()
        Sale.objects.create(customer=self.customer, amount=200, date="2024-06-01")
        url = reverse("sales-stats-daily")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_stats_customers(self):
        self.authenticate()
        Sale.objects.create(customer=self.customer, amount=200, date="2024-06-01")
        url = reverse("sales-stats-customers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("top_volume", response.data)
        self.assertIn("top_avg", response.data)
        self.assertIn("top_freq", response.data)
