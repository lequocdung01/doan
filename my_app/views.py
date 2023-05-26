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

def product_mypham(request):
    context = {}
    return render(request, 'html/category.html', context)

def event(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'html/event.html', context)

def contactus(request):
    context = {}
    return render(request, 'html/contactus.html', context)

def regestermember(request):
    context = {}
    return render(request, 'html/regestermember.html', context)

def memberkhuyenmai(request):
    context = {}
    return render(request, 'html/memberkhuyenmai.html', context)

def introduce(request):
    context = {}
    return render(request, 'html/introduce.html', context)

def TuyenDung(request):
    context = {}
    return render(request, 'html/TuyenDung.html', context)

def location(request):
    context = {}
    return render(request, 'html/location.html', context)

def form(request):
    context = {}
    return render(request, 'html/form.html', context)
