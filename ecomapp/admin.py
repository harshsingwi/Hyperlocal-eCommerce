from django.contrib import admin

# Register your models here.

from ecomapp.models import Product, Order

admin.site.register(Product) 
admin.site.register(Order)