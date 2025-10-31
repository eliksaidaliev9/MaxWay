from django.shortcuts import render,redirect
import json
from django.http import JsonResponse
from .models import *
from .services import *
from .forms import *
from config.settings import MEDIA_ROOT

def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)

def order_page(request):
    if request.GET:
        phone = request.GET.get("phone_number", "")
        email = request.GET.get("email", "")

        customer = get_customer_by_phone_email(phone, email) or {}
        return JsonResponse(customer)


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price",0)
    print(orders_list)
    print(total_price)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                "product": Product.objects.get(pk=int(key)),
                "count": val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders':orders,
        'total_price':total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }

    response = render(request, 'food/index.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response


def main_order(request):
    model = Customer()
    if request.POST:
        try:
            model = Customer.objects.get(
                phone_number=request.POST.get("phone_number"),
                email=request.POST.get("email")
            )
        except Customer.DoesNotExist:
            model = Customer()

        form = CustomerForm(request.POST or None, instance=model)
        if form.is_valid():
            customer = form.save()
            form_order = OrderForm(request.POST or None, instance=Order())
            if form_order.is_valid():
                order = form_order.save(customer=customer)
                print(order)
                order_list = request.COOKIES.get("orders")

                for key, val in json.loads(order_list).items():
                    product = get_product_by_id(int(key))
                    counts = val
                    order_product = OrderProduct(
                        count=counts,
                        price=product['price'],
                        product_id=product['id'],
                        order_id=order.id
                    )
                    order_product.save()
                response = redirect("index")
                response.delete_cookie("orders")
                response.delete_cookie("total_price")
                return response
            else:
                print(form_order.errors)
        else:
            print(form.errors)

    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price", 0)
    print(orders_list)
    print(total_price)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    "count": val
                }
            )
    ctx = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }

    response = render(request, 'food/order.html', ctx)
    response.set_cookie("greeting", 'hello')
    return response
