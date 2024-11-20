from django.urls import path, include
from ecomapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search_view, name='search'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('address/', views.address_view, name="address"),
    path('orders/', views.user_orders, name="orders"),
]
