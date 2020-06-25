from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from .decoratores import unauthenticated_user,allowed_users,admin_only
# Create your views here.
@unauthenticated_user
def registerform(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for'+  user)
            return redirect('login')

    context = {'form':form}
    return render(request, 'shopping/register.html',context)
@unauthenticated_user
def loginform(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username/Password is incorrect')

    context =  {}
    return render(request, 'shopping/login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'shopping/store.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        item = []

    context = {'items':items}
    return render(request, 'shopping/cart.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def checkout(request):
    return render(request, 'shopping/checkout.html')

def UserPage(request):
    return render(request, 'shopping/user.html')
