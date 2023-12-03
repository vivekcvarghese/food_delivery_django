from rest_framework import serializers
from .models import Product, User, OrderItem, Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CSVUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_blocked']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure the password field is write-only
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['item_name', 'quantity', 'order']

class OrderSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Order
        fields = ['id', 'status']

    # def update(self, instance, validated_data):
    #     items_data = validated_data.pop('items', [])
    #     instance.status = validated_data.get('status', instance.status)
    #     instance.save()

    #     # Update or create items
    #     for item_data in items_data:
    #         item, created = OrderItem.objects.update_or_create(
    #             order=instance,
    #             item_name=item_data['item_name'],
    #             defaults={'quantity': item_data['quantity']}
    #         )

    #     return instance