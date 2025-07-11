from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from customers.models import Customer


class CustomerAPITestCase(APITestCase):
    def setUp(self):
        # Criar um usuário para autenticação
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        # URL base da API customers
        self.url = reverse("customers-list")  # Usando DefaultRouter registra como 'customers-list'

        # Dados para criar um cliente
        self.customer_data = {"name": "João Silva", "email": "joao@example.com", "phone": "1234567890"}

    def authenticate(self):
        # Autenticar e armazenar token no header
        response = self.client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_auth_required(self):
        # Testa que autenticação é necessária
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_customer(self):
        self.authenticate()
        response = self.client.post(self.url, self.customer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().name, "João Silva")

    def test_list_customers(self):
        self.authenticate()
        Customer.objects.create(**self.customer_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_customer(self):
        self.authenticate()
        customer = Customer.objects.create(**self.customer_data)
        url_detail = reverse("customers-detail", args=[customer.id])
        new_data = {"name": "João Atualizado", "email": "joaoatualizado@example.com", "phone": "0987654321"}
        response = self.client.put(url_detail, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        customer.refresh_from_db()
        self.assertEqual(customer.name, "João Atualizado")

    def test_delete_customer(self):
        self.authenticate()
        customer = Customer.objects.create(**self.customer_data)
        url_detail = reverse("customers-detail", args=[customer.id])
        response = self.client.delete(url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)
