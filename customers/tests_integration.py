from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CustomerIntegrationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="integration", password="integration123")
        self.auth_url = reverse("token_obtain_pair")
        self.customers_url = reverse("customers-list")

    def authenticate(self):
        response = self.client.post(self.auth_url, {"username": "integration", "password": "integration123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_full_customer_flow(self):
        # Autentica
        self.authenticate()
        # Cria cliente
        data = {"name": "Cliente Integração", "email": "int@example.com", "phone": "999999999"}
        response = self.client.post(self.customers_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Lista clientes
        response = self.client.get(self.customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(c["email"] == "int@example.com" for c in response.data))
