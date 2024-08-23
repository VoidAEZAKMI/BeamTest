from rest_framework import viewsets
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from web.models import Product, Category, Supplier, Order
from .serializers import ProductSerializer, CategorySerializer, SupplierSerializer, OrderSerializer
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.shortcuts import render




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notifications", {
                "type": "send_notification",
                "message": f"New product created: {instance.name}"
            }
        )



# Swagger схема и UI
schema_view = get_schema_view(
    openapi.Info(
        title="Test API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

