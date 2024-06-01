from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem

def index(request):
    products=Product.objects.all()
    order = get_user_order(request)
    
    # Get the total number of items in the cart
    item_count = order.items.count()
    return render(request,'index.html',{'products':products,'item_count': item_count})


def get_user_order(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, is_ordered=False)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        order, created = Order.objects.get_or_create(session_key=request.session.session_key, is_ordered=False)
    return order

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = get_user_order(request)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        order_item.quantity += 1
        order_item.save()
    
    return redirect('index')

def view_cart(request):
    order = get_user_order(request)
    return render(request, 'cart.html', {'order': order})

def update_cart(request, item_id, action):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if action == 'increase':
        order_item.quantity += 1
    elif action == 'decrease':
        order_item.quantity -= 1
        if order_item.quantity == 0:
            order_item.delete()
            return redirect('view_cart')
    order_item.save()
    return redirect('view_cart')

def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_item.delete()
    return redirect('view_cart')

@login_required
def checkout(request):
    order = get_user_order(request)
    total_price=0
    for item in order.items.all():
        print(f"price:{item.quantity}")
        total_price = total_price+(item.product.price * item.quantity)
    print(total_price)
    if request.method == 'POST':
        order.is_ordered = True
        
        order.save()
        return redirect('order_success')
    return render(request, 'checkout.html', {'order': order, 'total_price': total_price})

@login_required
def order_success(request):
    return render(request, 'order_success.html')



@login_required
def profile(request):
    if request.user.is_authenticated:
        # Access user details
        return render(request,'profile.html',{'user':request.user})