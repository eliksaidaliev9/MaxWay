from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from food.models import *
from . import forms
from . import services

def login_required_decorator(func):
    return login_required(func,login_url='login_page')


def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,  password=password,)
        if user is not None:
            login(request, user)
            return redirect("main_page")
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, 'dashboard/login.html')


@login_required_decorator
def logout_page(request):
    logout(request)
    return redirect("login_page")


@login_required_decorator
def main_page(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_products = []
    table_list = services.get_table()
    print(table_list)

    for category in categories:
        order_products.append(
            {
                "category": category.title,
                "product": len(Product.objects.filter(category_id=category.id))
            }
        )

    ctx={
        'counts' : {
            'categories':len(categories),
            'products':len(products),
            'customers':len(customers),
            'orders':len(orders),
        },
        'order_products': order_products,
        'table_list': table_list,

    }
    return render(request, 'dashboard/index.html', ctx)

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login_page")
    template_name = "dashboard/signup.html"


# CATEGORY
@login_required_decorator
def category_create(request):
    model = Category()
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        category_count = request.session.get('category_count', 0)
        category_count += 1
        request.session["category_count"] = category_count
        return redirect('category_list')
    ctx = {
        "model":model,
        "form":form
    }
    return render(request,'dashboard/category/form.html',ctx)

@login_required_decorator
def category_edit(request,pk):
    model = Category.objects.get(pk=pk)
    form = forms.CategoryForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        return redirect('category_list')
    ctx = {
        "model":model,
        "form":form
    }
    return render(request,'dashboard/category/form.html',ctx)

@login_required_decorator
def category_delete(request,pk):
    model = Category.objects.get(pk=pk)
    model.delete()

    category_count = request.session.get('category_count', 0)
    if category_count > 0:
        category_count -= 1
        request.session["category_count"] = category_count
    return redirect('category_list')

@login_required_decorator
def category_list(request):
    categories = Category.objects.all()

    ctx={
        "categories":categories
    }
    return render(request,'dashboard/category/list.html',ctx)

# PRODUCT
@login_required_decorator
def product_create(request):
    model = Product()
    form = forms.ProductForm(request.POST or None,request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        product_count = request.session.get('product_count', 0)
        product_count +=1
        request.session["product_count"] = product_count

        return redirect('product_list')


    ctx = {
        "model":model,
        "form":form
    }
    return render(request,'dashboard/product/form.html',ctx)

@login_required_decorator
def product_edit(request,pk):
    model = Product.objects.get(pk=pk)
    form = forms.ProductForm(request.POST or None,request.FILES or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        return redirect('product_list')

    ctx = {
        "model":model,
        "form":form
    }
    return render(request,'dashboard/product/form.html',ctx)

@login_required_decorator
def product_delete(request,pk):
    model = Product.objects.get(pk=pk)
    model.delete()

    product_count = request.session.get('product_count', 0)
    if product_count > 0:
        product_count -= 1
        request.session["product_count"] = product_count

    return redirect('product_list')

@login_required_decorator
def product_list(request):
    products = Product.objects.all
    ctx={
        "products":products
    }
    return render(request,'dashboard/product/list.html',ctx)

#CUSTOMER
@login_required_decorator
def customer_create(request):
    model = Customer()
    form = forms.CustomerForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        customer_count = request.session.get('customer_count', 0)
        customer_count += 1
        request.session["customer_count"] = customer_count

        return redirect('customer_list')
    ctx = {
        "model":model,
        "form":form
    }
    return render(request,'dashboard/customer/form.html',ctx)

@login_required_decorator
def customer_edit(request,pk):
    model = Customer.objects.get(pk=pk)
    form = forms.CustomerForm(request.POST or None, instance=model)
    if request.POST and form.is_valid():
        form.save()

        return redirect('customer_list')
    ctx = {
        "model":model,
        "form":form
    }
    return render(request,'dashboard/customer/form.html',ctx)

@login_required_decorator
def customer_delete(request,pk):
    model = Customer.objects.get(pk=pk)
    model.delete()

    customer_count = request.session.get('customer_count', 0)
    if customer_count > 0:
        customer_count -= 1
        request.session["customer_count"] = customer_count

    return redirect('customer_list')

@login_required_decorator
def customer_list(request):
    customers = Customer.objects.all()
    ctx={
        "customers":customers
    }
    return render(request,'dashboard/customer/list.html',ctx)



@login_required_decorator
def order_list(request):
    orders = Order.objects.all()
    ctx={
        "orders":orders
    }
    return render(request,'dashboard/order/list.html',ctx)


@login_required_decorator
def customer_order_list(request,id):
    customer_orders = services.get_order_by_user(id=id)
    ctx = {
        'customer_orders': customer_orders
    }
    return render(request, "dashboard/customer_order/list.html", ctx)



@login_required_decorator
def order_product_list(request, id):
    order_products = services.get_product_by_order(id=id)
    ctx={
        "order_products": order_products
    }
    return render(request,'dashboard/order_product/list.html',ctx)

