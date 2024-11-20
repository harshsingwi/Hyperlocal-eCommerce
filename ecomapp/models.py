from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="", default="")

    def __str__(self):
        return self.product_name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    email = models.EmailField(max_length=254)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(blank=True, max_length=255, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
