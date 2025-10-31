from django.urls import path
from .views import *

urlpatterns = [
    path('',main_page, name='main_page'),
    path('login_page/',login_page, name='login_page'),
    path('logout_page/',logout_page, name='logout_page'),
    path('signup/', SignUpView.as_view(), name='signup'),

    path('category/create/',category_create, name='category_create'),
    path('category/<int:pk>/edit/',category_edit, name='category_edit'),
    path('category/<int:pk>/delete/',category_delete, name='category_delete'),
    path('category/list/',category_list, name='category_list'),

    path('product/create/',product_create, name='product_create'),
    path('product/<int:pk>/edit/',product_edit, name='product_edit'),
    path('product/<int:pk>/delete/',product_delete, name='product_delete'),
    path('product/list/',product_list, name='product_list'),

    path('customer/create/',customer_create, name='customer_create'),
    path('customer/<int:pk>/edit/',customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/',customer_delete, name='customer_delete'),
    path('customer/list/',customer_list, name='customer_list'),


    path('order/list/',order_list, name='order_list'),
    path('customer_order/<int:id>/list/', customer_order_list, name="customer_order_list"),
    path('order_product/<int:id>/list/', order_product_list, name='order_product_list'),

]