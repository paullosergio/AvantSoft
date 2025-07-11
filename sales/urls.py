from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SaleViewSet

router = DefaultRouter()
router.register("", SaleViewSet, basename="sales")

urlpatterns = [
    path("", include(router.urls)),
]
