from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tags.models import Tag

class Customer(models.Model):
  customer_id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True)
  phone_number = models.CharField(max_length=20, blank=True, null=True)

  def __str__(self):
    return self.user.username

class Product(models.Model):
  product_id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  inventory = models.IntegerField()
  last_update = models.DateTimeField(default=timezone.now)
  Collection_id = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name='products')
  tags = models.ManyToManyField(Tag,blank=True,related_name='products')

class Collection(models.Model):
  collection_id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

class Order(models.Model):  
  order_id = models.AutoField(primary_key=True)
  customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='orders')
  placed_at = models.DateTimeField(default=timezone.now)
  payment_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('complete', 'Complete'), ('failed', 'Failed')], default='pending')

class OrderItem(models.Model):  
  order_item_id = models.AutoField(primary_key=True)
  order_id = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
  product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_items')
  quantity = models.IntegerField()
  unit_price = models.DecimalField(max_digits=10, decimal_places=2)

class Cart(models.Model):
  cart_id = models.AutoField(primary_key=True)
  created_at = models.DateTimeField(default=timezone.now)

class CartItem(models.Model):
  cart_item_id = models.AutoField(primary_key=True)
  cart_id = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
  product_id = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cart_items')
  quantity = models.IntegerField()