from django.shortcuts import render
from .models import *
from django.http import HttpResponse
# Create your views here.
def get_my_app(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request,'html/home.html',context)

def detail(request):
    context={}
    return render(request,'html/detail_product.html',context)

def cart(request):
    context={}
    return render(request, 'html/cart.html', context)

def cart(request):
    context={}
    return render(request, 'html/cart.html', context)

def product_mypham(request):
    context = {}
    return render(request, 'html/product.html', context)

def event(request):
    context = {}
    return render(request, 'html/event.html', context)
