from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauth_user, allow_users, admin_only

# Create your views here.
@unauth_user
def registerPage(request):
    form = CreateUserForm()
    if(request.method == "POST"):
        form = CreateUserForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account has been created ' + username)
            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)

@unauth_user
def loginPage(request):
    if(request.method == "POST"):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if(user is not  None):
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "usernames or password is wrong")

    context = {}
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }

    return render(request, 'accounts/dasboard.html', context)

@login_required(login_url='login')
@allow_users(allow_roles=['admin', 'customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders': orders,
        'total_orders': total_orders,
        'delivered': delivered,
        'pending': pending,
    }
    return render(request, 'accounts/user_page.html', context)

@login_required(login_url='login')
@allow_users(allow_roles=['admin', 'customer'])
def account_settings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if(request.method == "POST"):
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if(form.is_valid()):
            form.save()

    context = {
        'form': form
    }

    return render(request, 'accounts/account_setting.html', context)

@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'accounts/product.html', context)

@login_required(login_url='login')
@admin_only
def custumer(request, pk):
    customer = Customer.objects.get(id = pk)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'order_count': order_count,
        'myFilter': myFilter,
    }

    return render(request, 'accounts/custumer.html', context)

@login_required(login_url='login')
@admin_only
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id = pk)
    formSet = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})

    if(request.method == 'POST'):
        # form = OrderForm(request.POST)
        formSet = OrderFormSet(request.POST, instance=customer)
        if(formSet.is_valid()):
            formSet.save()
            return redirect('/')

    context = {
        'formSet': formSet
    }

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@admin_only
def updateOrder(request, pk):
    order = Order.objects.get(id = pk)
    form = OrderForm(instance=order)

    if(request.method == 'POST'):
        form = OrderForm(request.POST, instance=order)

        if(form.is_valid()):
            form.save()
            return redirect('/')
    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@admin_only
def deleteOrder(request, pk):
    order = Order.objects.get(id = pk)
    if(request.method == "POST"):
        order.delete()
        return redirect('/')
    context = {
        'order': order
    }

    return render(request, 'accounts/delete.html', context)