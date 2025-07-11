from django.db import models

from customers.models import Customer

# Create your models here.


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} - {self.amount} em {self.date}"
