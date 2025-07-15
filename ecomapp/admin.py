from django.contrib import admin

# Register your models here.

from ecomapp.models import Product, Order, Address

admin.site.register(Product) 
admin.site.register(Order)
admin.site.register(Address)