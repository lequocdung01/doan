from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# trang chu
def get_my_app(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    product = Product.objects.all()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(product, 6)  # hiện số lượng sản phẩm
    paged_products = paginator.get_page(page)
    page_obj = product.count()
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories,'product': product,'cartItems':cartItems,'user_login':user_login, 'user_logout':user_logout,'paged_products':paged_products,'page_obj':page_obj}
    return render(request,'html/home.html',context)
# chi tiết sản phẩm
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(ID=id)
    categories = Category.objects.filter(is_sub=False)
    context={'categories': categories,'products': products,'user_login':user_login,'user_logout':user_logout,'cartItems':cartItems}
    return render(request,'html/detail.html',context)
# 
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context={'items':items, 'order':order, 'user_login':user_login, 'user_logout':user_logout,"cartItems":cartItems}
    return render(request, 'html/cart.html', context)

#Thanh toan
def delivery(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context = {'items': items, 'order': order, 'user_login':user_login, 'user_logout':user_logout,"cartItems":cartItems}
    return render(request, 'html/delivery.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user
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
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request, 'html/payment.html', context)

# trang sản phẩm
def product(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    product = Product.objects.all()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(product, 10)  # hiện số lượng sản phẩm
    paged_products = paginator.get_page(page)
    page_obj = product.count()
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories,'product': paged_products, 'page_obj': page_obj,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request, 'html/product.html', context=context)

# Tran san pham
def category(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories': categories,'products':products,'active_category':active_category,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request,'html/category.html', context)

# trang tìm kiếm
def search(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    searched = None
    keys = None
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)

    context = {"searched":searched, "keys":keys, "categories": categories, 'active_category':active_category,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems }
    
    return render(request, 'html/search.html', context)

# trang sự kiện
def event(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    product = Product.objects.all()
    context = {'product': product,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
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
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request, 'html/memberkhuyenmai.html', context)
# trang giới thiệu
def introduce(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request, 'html/introduce.html', context)
# trang tuyển dụng
def TuyenDung(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request, 'html/TuyenDung.html', context)
# trang địa chỉ
def location(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems}
    return render(request, 'html/location.html', context)
# trang đăng ký
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            messages.error(request=request,message='Tên đăng nhập đã tồn tại!')
    context = {"form":form}
    return render(request, 'html/register.html', context)
# trang dang nhap
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,message='Tên Đăng Nhập Hoặc Mật Khẩu Không Đúng!')
    context = {}
    return render(request,'html/loginPage.html',context)
# trang dang xuat
def logoutPage(request):
    logout(request)
    messages.success(request=request,message='Bạn đã đăng xuất thành công!')
    return redirect('login')

