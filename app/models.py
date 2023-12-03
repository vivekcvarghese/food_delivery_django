from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()


class User(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('agent', 'Agent'),
        ('customer', 'Customer'),
    ]

    username = models.CharField(max_length=120, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=600, null=False, blank=False)
    role = models.CharField(max_length=50, null=False, blank=False, choices=ROLES)
    is_blocked = models.BooleanField(default=False)

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        return check_password(password, self.password)

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

class OrderItem(models.Model):
    id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=120, null=False, blank=False)
    quantity = models.IntegerField(null=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)