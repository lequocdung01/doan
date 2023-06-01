from django.shortcuts import render,redirect
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
def get_my_app(request):
    product = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories,'product': product}
    return render(request,'html/home.html',context)
# chi tiết sản phẩm
def detail(request):
    context={}
    return render(request,'html/detail_product.html',context)
# 
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
    context={'items':items, 'order':order}
    return render(request, 'html/cart.html', context)

#Thanh toan
def delivery(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
    context = {'items': items, 'order': order}
    return render(request, 'html/delivery.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(ID = productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action=='add':
        orderItem.quantity +=1
    elif action == 'remove':
        orderItem.quantity -=1
    orderItem.save()
    if orderItem.quantity <=0:
        orderItem.delete()
    return JsonResponse('added',safe=False)

#Thanh toan
def payment(request):
    context = {}
    return render(request, 'html/payment.html', context)

# trang sản phẩm
def product(request):
    product = Product.objects.all()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(product, 10)  # hiện số lượng sản phẩm
    paged_products = paginator.get_page(page)
    page_obj = product.count()

    context = {'product': paged_products, 'page_obj': page_obj}
    return render(request, 'html/product.html', context=context)

# Tran san pham
def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories': categories,'products':products,'active_category':active_category}
    return render(request,'html/category.html', context)

# trang tìm kiếm
def search(request):
    searched = None
    keys = None
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)

    context = {"searched":searched, "keys":keys, "categories": categories, 'active_category':active_category }
    
    return render(request, 'html/search.html', context)

# trang sự kiện
def event(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'html/event.html', context)
# trang liên hệ
def contactus(request):
    context = {}
    return render(request, 'html/contactus.html', context)
# trang đăng ký thành viên 
def regestermember(request):
    context = {}
    return render(request, 'html/regestermember.html', context)
# trang khuyến mãi
def memberkhuyenmai(request):
    context = {}
    return render(request, 'html/memberkhuyenmai.html', context)
# trang giới thiệu
def introduce(request):
    context = {}
    return render(request, 'html/introduce.html', context)
# trang tuyển dụng
def TuyenDung(request):
    context = {}
    return render(request, 'html/TuyenDung.html', context)
# trang địa chỉ
def location(request):
    context = {}
    return render(request, 'html/location.html', context)
# trang đăng ký
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {"form":form}
    return render(request, 'html/register.html', context)
# trang dang nhap
def loginPage(request):
    if request.user.is_autheticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Tên Đăng Nhập Hoặc Mật Khẩu Không Đúng!')
    context = {}
    return render(request,'html/form.html',context)