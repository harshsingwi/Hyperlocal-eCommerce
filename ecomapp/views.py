from django.shortcuts import render, get_object_or_404, redirect
from ecomapp.models import Product, Order, Address,OrderItem
from math import ceil
from django.db.models import Q
from django.contrib import messages
from .forms import OrderForm
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

PRODUCTS_PER_SLIDE = 4

def normalize_product(product, is_api_product=False):
    """Normalize product data structure between DB and API products"""
    if is_api_product:
        return {
            'product_id': product.get('id'),
            'product_name': product.get('title', 'Unknown Product'),  # API uses 'title'
            'category': product.get('category', 'Other'),
            'sub_category': '',  # API doesn't have sub_category
            'price': int(product.get('price', 0)),  # Convert to int to match your model
            'desc': product.get('description', ''),
            'image': product.get('image', ''),
            'pub_date': None,  # API doesn't have pub_date
            'is_api_product': True
        }
    return {
        'product_id': product.id,
        'product_name': product.product_name,
        'category': product.category,
        'sub_category': product.sub_category,
        'price': product.price,
        'desc': product.desc,
        'image': product.image.url if product.image else '',
        'pub_date': product.pub_date,
        'is_api_product': False
    }

def fetch_api_products():
    """Fetch products from external API"""
    try:
        response = requests.get("https://fakestoreapi.com/products", timeout=30)
        response.raise_for_status()
        return [normalize_product(product, is_api_product=True) for product in response.json()]
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching API products: {e}")
        return []

def home(request):
    # Initialize empty lists and sets for products
    allProds = []
    all_categories = set()
    combined_products = []
    
    # Get local database products
    try:
        catprods = Product.objects.values('category').distinct()
        db_categories = {item['category'] for item in catprods}
        all_categories.update(db_categories)
        
        # Get and normalize database products
        db_products = Product.objects.all()
        combined_products.extend([normalize_product(product) for product in db_products])
    except ObjectDoesNotExist as e:
        print(f"Error fetching database products: {e}")
    
    # Get API products
    api_products = fetch_api_products()
    if api_products:
        api_categories = {product['category'] for product in api_products}
        all_categories.update(api_categories)
        combined_products.extend(api_products)
    
    # Group products by category
    for category in all_categories:
        category_products = [p for p in combined_products if p['category'] == category]
        if category_products:
            n = len(category_products)
            nSlides = ceil(n / PRODUCTS_PER_SLIDE)
            allProds.append({
                'category': category,
                'products': category_products,
                'range': range(1, nSlides + 1),
                'nSlides': nSlides
            })
    
    params = {
        'allProds': allProds,
        'error': None if combined_products else "No products available at the moment."
    }
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
    api_results = []

    # Search in database
    if query:
        results = Product.objects.filter(
            Q(product_name__icontains=query) |
            Q(category__icontains=query) |
            Q(sub_category__icontains=query)
        )
    
    # Search in API
    if query:
        try:
            response = requests.get(f'https://fakestoreapi.com/products', timeout=30)
            response.raise_for_status()
            api_products = response.json()
            
            # Filter API results for the query
            api_results = [
                product for product in api_products
                if query.lower() in product['title'].lower() or
                   query.lower() in product.get('category', '').lower()
            ]
        except requests.exceptions.RequestException as e:
            print(f"Error fetching API products: {e}")

    context = {
        'query': query,
        'results': results,
        'api_results': api_results,
    }
    return render(request, 'search_results.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def address_view(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_address':
            # Handle new address creation
            address = Address.objects.create(
                user=request.user,
                name=request.POST['name'],
                surname=request.POST['surname'],
                address1=request.POST['address1'],
                address2=request.POST['address2'],
                city=request.POST['city'],
                state=request.POST['state'],
                zip_code=request.POST['zip_code'],
                phone=request.POST['phone'],
            )
            if request.POST.get('make_default'):
                Address.objects.filter(user=request.user).update(is_default=False)
                address.is_default = True
                address.save()
                
        elif action == 'select_address':
            # Get the selected address
            address_id = request.POST.get('address_id')
            selected_address = Address.objects.get(id=address_id)
            
            # Get cart data from the POST request
            cart_data = json.loads(request.POST.get('cart_data', '{}'))
            
            if not cart_data:
                messages.error(request, "Your cart is empty!")
                return redirect('cart')
            
            # Calculate total from cart data
            total_amount = sum(
                float(item['price']) * int(item['quantity']) 
                for item in cart_data.values()
            )
            
            # Create order with COD as default payment method
            order = Order.objects.create(
                user=request.user,
                address=selected_address,
                total_amount=total_amount,
                status='CONFIRMED',  # Changed from 'PENDING' to 'CONFIRMED'
                payment_method='COD'  # Set COD as default payment method
            )
            
            # Create order items
            for product_id, item in cart_data.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=float(item['price'])
                )
            
            messages.success(request, "Order placed successfully!")
            return redirect('order_success')
                
        elif action == 'make_default':
            address_id = request.POST.get('address_id')
            Address.objects.filter(user=request.user).update(is_default=False)
            Address.objects.filter(id=address_id).update(is_default=True)
    
    saved_addresses = Address.objects.filter(user=request.user)
    return render(request, 'address.html', {'saved_addresses': saved_addresses})

@login_required
def order_success(request):
    order = Order.objects.get(id=request.session.get('order_id'))
    return render(request, 'order_success.html', {'order': order})

def user_orders(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders.html', {'orders': orders})
    else:
        return redirect('home')
