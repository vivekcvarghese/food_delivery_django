from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import Product, User, OrderItem, Order
from .serializers import ProductSerializer, CSVUploadSerializer, UserSerializer, OrderItemSerializer, OrderSerializer
from io import StringIO
import csv

class ProductDetail(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(product)
            return Response({'message': 'Product details', 'product': serializer.data})
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Product updated successfully'})
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return Response({'message': 'Product deleted successfully'})
        except Product.DoesNotExist:
            return Response({'message': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Product added successfully', 'product_id': serializer.data['id']}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({'message': 'Product list', 'products': serializer.data})

    # parser_classes = [parsers.MultiPartParser]

    def post(self, request):
        serializer = CSVUploadSerializer(data=request.data)
        if serializer.is_valid():
            csv_file = serializer.validated_data['file']
            self.process_csv(csv_file)
            return Response({'message': 'Bulk upload successful'})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def process_csv(self, csv_file):
        csv_data = csv.reader(StringIO(csv_file.read().decode('utf-8')))
        header = next(csv_data)

        for row in csv_data:
            # Assuming CSV format: name,price
            name, price = row
            Product.objects.create(name=name, price=float(price))


class AddUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User added successfully', 'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_blocked = True
        user.save()
        return Response({'message': 'User blocked successfully'})

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class OrderResource(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            items_data = request.data.get('items', [])
            for item_data in items_data:
                item_data['order'] = order.id
                item_serializer = OrderItemSerializer(data=item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        serializer = OrderSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Clear existing items
            OrderItem.objects.filter(order_id=order.id).delete()
            # Add new items
            items_data = request.data.get('items', [])
            for item_data in items_data:
                item_data['order'] = order.id
                item_serializer = OrderItemSerializer(data=item_data)
                if item_serializer.is_valid():
                    item_serializer.save()
                else:
                    return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': f'Order {order_id} updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        items = OrderItem.objects.filter(order_id=order.id)
        order_serializer = OrderSerializer(order)
        item_serializer = OrderItemSerializer(items, many=True)
        order_details = {
            'order': order_serializer.data,
            'items': item_serializer.data
        }
        return Response(order_details)

    