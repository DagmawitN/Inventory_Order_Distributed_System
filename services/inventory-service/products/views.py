from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    @action(detail=True, methods=['patch'], url_path='update-stock')
    def update_stock(self, request, pk=None):
        product = self.get_object()
        quantity = request.data.get('stock_quantity')

        if quantity is None:
            return Response(
                {"error": "stock_quantity is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if int(quantity) < 0:
            return Response(
                {"error": "stock_quantity cannot be negative"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.stock_quantity = quantity
        product.save()

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
