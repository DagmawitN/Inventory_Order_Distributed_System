from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .inventory_client import check_inventory, update_inventory
from .rabbitmq import publish_order_completed

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        
        items_data = request.data.get('items', [])
        if not items_data:
            return Response({'error': 'No items in order'}, status=status.HTTP_400_BAD_REQUEST)

        for item in items_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            if not check_inventory(product_id, quantity):
                return Response(
                    {'error': f'Insufficient stock for product {product_id}'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        for item in items_data:
            product_id = item.get('product_id')
            quantity = item.get('quantity')
            update_inventory(product_id, -quantity) 
        
        publish_order_completed(serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['put'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = new_status
        order.save()
        
        if new_status == 'COMPLETED':
            publish_order_completed(OrderSerializer(order).data)
            
        return Response(OrderSerializer(order).data)
