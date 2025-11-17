from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Q
from .models import Shopkeeper, Customer, Due
from datetime import date

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        shop_name = request.POST.get('shop_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        Shopkeeper.objects.create(
            user=user,
            shop_name=shop_name,
            phone_number=phone_number,
            address=address
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    shopkeeper = request.user.shopkeeper
    customers = Customer.objects.filter(shopkeeper=shopkeeper)
    
    total_customers = customers.count()
    total_pending_dues = Due.objects.filter(
        customer__shopkeeper=shopkeeper, 
        status='PENDING'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    recent_dues = Due.objects.filter(
        customer__shopkeeper=shopkeeper
    ).select_related('customer')[:10]

    context = {
        'shopkeeper': shopkeeper,
        'total_customers': total_customers,
        'total_pending_dues': total_pending_dues,
        'recent_dues': recent_dues,
    }
    return render(request, 'dashboard.html', context)

@login_required
def customers_view(request):
    shopkeeper = request.user.shopkeeper
    search_query = request.GET.get('search', '')
    
    customers = Customer.objects.filter(shopkeeper=shopkeeper)
    if search_query:
        customers = customers.filter(
            Q(customer_name__icontains=search_query) | 
            Q(phone_number__icontains=search_query)
        )

    context = {'customers': customers, 'search_query': search_query}
    return render(request, 'customers.html', context)

@login_required
def add_customer_view(request):
    if request.method == 'POST':
        shopkeeper = request.user.shopkeeper
        customer_name = request.POST.get('customer_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address', '')

        Customer.objects.create(
            shopkeeper=shopkeeper,
            customer_name=customer_name,
            phone_number=phone_number,
            address=address
        )
        messages.success(request, 'Customer added successfully')
        return redirect('customers')

    return render(request, 'add_customer.html')

@login_required
def customer_detail_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, shopkeeper=request.user.shopkeeper)
    dues = customer.dues.all()
    total_pending = customer.total_dues()

    context = {
        'customer': customer,
        'dues': dues,
        'total_pending': total_pending
    }
    return render(request, 'customer_detail.html', context)

@login_required
def add_due_view(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, shopkeeper=request.user.shopkeeper)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        Due.objects.create(
            customer=customer,
            amount=amount,
            description=description,
            due_date=due_date,
            status='PENDING'
        )
        messages.success(request, 'Due added successfully')
        return redirect('customer_detail', customer_id=customer.id)

    context = {'customer': customer}
    return render(request, 'add_due.html', context)

@login_required
def mark_paid_view(request, due_id):
    due = get_object_or_404(Due, id=due_id, customer__shopkeeper=request.user.shopkeeper)
    due.status = 'PAID'
    due.save()
    messages.success(request, 'Due marked as paid')
    return redirect('customer_detail', customer_id=due.customer.id)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
