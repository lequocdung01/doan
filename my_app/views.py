from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator

# Create your views here.
def get_my_app(request):
    product = Product.objects.all()
    context = {'product': product}
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
    context={'items':items, 'order':order}
    return render(request, 'html/cart.html', context)
# trang sản phẩm
def product(request):
    product = Product.objects.all()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(product, 10)  # hiện số lượng sản phẩm
    paged_products = paginator.get_page(page)
    page_obj = product.count()

    context = {'product': paged_products, 'page_obj': page_obj}
    return render(request, 'html/category.html', context=context)
# trang mỹ phẩm
def product_mypham(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'html/category.html', context)
# trang tìm kiếm
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    return render(request, 'html/search.html', {"searched":searched, "keys":keys })
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
# trang đăng nhập/ đăng ký
def form(request):
    context = {}
    return render(request, 'html/form.html', context)
