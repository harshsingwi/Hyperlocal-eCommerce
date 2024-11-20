from django.shortcuts import render, get_object_or_404, redirect
from ecomapp.models import Product, Order
from math import ceil
from django.db.models import Q
from django.contrib import messages
from .forms import OrderForm


PRODUCTS_PER_SLIDE = 4

def home(request):
    allProds = []
    catprods = Product.objects.values('category').distinct()
    categories = {item['category'] for item in catprods}
    
    for category in categories:
        products = Product.objects.filter(category=category)
        n = len(products)
        nSlides = ceil(n / PRODUCTS_PER_SLIDE)
        allProds.append([products, range(1, nSlides + 1), nSlides])
    
    params = {'allProds': allProds}
    return render(request, 'index.html', params)

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login and Try Again")
        return redirect('/ecomauth/login/')
    return render(request, 'checkout.html')

def search_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query) |
            Q(sub_category__icontains=query)
        )
    return render(request, 'search_results.html', {'query': query, 'results': results})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

def address_view(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        cart_total = request.POST.get('cart_total', '0')
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.amount = cart_total
            order.save()
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'address.html', {'form': form})


def user_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders.html', {'orders': orders})
    else:
        return redirect('home')
