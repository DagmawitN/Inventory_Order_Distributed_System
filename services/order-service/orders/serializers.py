from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'total_price', 'status', 'items', 'created_at']
        read_only_fields = ['total_price', 'status', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Calculate total price
        total_price = sum(item['price'] * item['quantity'] for item in items_data)
        
        order = Order.objects.create(total_price=total_price, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
