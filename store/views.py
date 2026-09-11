from django.shortcuts import get_object_or_404, render
from django.db.models import Sum

from tags.models import Tag
from .models import CartItem, Collection, Order, Product


def home(request):
    return render(request, 'home.html')


def product_list(request):
    return render(request, 'store/product_list.html')


def product_detail(request, product_id):
    return render(request, 'store/product_detail.html')


def cart(request):
    return render(request, 'store/cart.html')


def checkout(request):

    return render(request, 'store/checkout.html')


def orders(request):

    return render(request, 'store/orders.html')
