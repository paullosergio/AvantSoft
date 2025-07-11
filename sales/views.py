from django.db.models import Avg, Count, Sum
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from customers.models import Customer

from .models import Sale
from .serializers import SaleSerializer

# Create your views here.


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="stats/daily")
    def stats_daily(self, request):
        # Total de vendas por dia
        sales_by_day = Sale.objects.values("date").annotate(total=Sum("amount")).order_by("date")
        return Response(list(sales_by_day))

    @action(detail=False, methods=["get"], url_path="stats/customers")
    def stats_customers(self, request):
        # Cliente com maior volume de vendas
        top_volume = (
            Customer.objects.annotate(total=Sum("sales__amount"))
            .order_by("-total")
            .values("id", "name", "total")
            .first()
        )
        # Cliente com maior média de valor por venda
        top_avg = (
            Customer.objects.annotate(avg=Avg("sales__amount")).order_by("-avg").values("id", "name", "avg").first()
        )
        # Cliente com maior número de dias únicos com vendas
        top_freq = (
            Customer.objects.annotate(days=Count("sales__date", distinct=True))
            .order_by("-days")
            .values("id", "name", "days")
            .first()
        )
        return Response(
            {
                "top_volume": top_volume,
                "top_avg": top_avg,
                "top_freq": top_freq,
            }
        )
