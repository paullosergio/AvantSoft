from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SaleIntegrationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="integration", password="integration123")
        self.auth_url = reverse("token_obtain_pair")
        self.customers_url = reverse("customers-list")
        self.sales_url = reverse("sales-list")

    def authenticate(self):
        response = self.client.post(self.auth_url, {"username": "integration", "password": "integration123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_full_sale_flow_and_stats(self):
        self.authenticate()
        # Cria cliente
        customer_data = {"name": "Cliente Venda", "email": "venda@example.com", "phone": "888888888"}
        response = self.client.post(self.customers_url, customer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        customer_id = response.data["id"]
        # Cria venda
        sale_data = {"customer": customer_id, "amount": "150.00", "date": "2024-06-02"}
        response = self.client.post(self.sales_url, sale_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Consulta estatísticas diárias
        url = reverse("sales-stats-daily")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))
        # Consulta estatísticas de clientes
        url = reverse("sales-stats-customers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("top_volume", response.data)
