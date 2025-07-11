from rest_framework import serializers

from .models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ["id", "customer", "amount", "date", "created_at"]
