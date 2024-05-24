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
from .forms import *
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg
from django.http import HttpResponse  # Import HttpResponse từ django.http
from django.db import IntegrityError

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import render
from .forms import ContactForm
import smtplib
# Create your views here.

# trang lịch sử mua hàng
@login_required
def history(request):
    customer = request.user
    completed_orders = Order.objects.filter(customer=customer, complete=True)
    
    # Truy xuất tất cả các sản phẩm từ các đơn hàng đã hoàn thành
    order_items = OrderItem.objects.filter(order__in=completed_orders).select_related('product')
    
    # Tạo danh sách các sản phẩm đã mua với các chi tiết cần thiết
    purchased_items = []
    for item in order_items:
        shipping_address = ShippingAddress.objects.filter(order=item.order).first()
        purchased_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item.get_total,
            'date_added': shipping_address.date_added if shipping_address else None,
        })
    
    context = {
        'purchased_items': purchased_items,
    }
    
    return render(request, 'html/history.html', context)

# trang chu
def get_my_app(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    
    product = Product.objects.all()
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(product, 6)  # hiện số lượng sản phẩm
    paged_products = paginator.get_page(page)
    page_obj = product.count()
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories,'product': product,'cartItems':cartItems,'user_login':user_login, 'user_logout':user_logout,'paged_products':paged_products,'page_obj':page_obj,'user_staff':user_staff, 'user':request.user}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    prod_id = request.GET.get('id', '')
    product = Product.objects.get(ID=prod_id)
    
    # Lấy giá trị trung bình của rate từ các đánh giá của sản phẩm
    avg_rate = Review.objects.filter(product=product).aggregate(Avg('rate'))['rate__avg'] or 0
    reviews = Review.objects.filter(product=product)

    products = Product.objects.filter(ID=prod_id)
    categories = Category.objects.filter(is_sub=False)
    context = {
        'categories': categories,
        'products': products,
        'user_login': user_login,
        'user_logout': user_logout,
        'cartItems': cartItems,
        'user_staff': user_staff,
        'avg_rate': avg_rate,  # Truyền giá trị trung bình rate vào context
        'reviews': reviews,
    }
    return render(request, 'html/detail.html', context)

# xu ly Review
def Review_rate(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(ID=prod_id)
        comment = request.GET.get('comment')
        rate = request.GET.get('star')
        created_at = timezone.now()  # Lấy ngày hiện tại
        user = request.user
        Review(user=user, product=product, comment=comment, rate=rate, created_at=created_at).save()
        # Sử dụng reverse để xây dựng URL của trang detail và truyền prod_id qua kwargs
        detail_url = reverse('detail')
        return redirect(detail_url + f'?id={prod_id}')


# 
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item':0,'get_cart_total':0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context={'items':items, 'order':order, 'user_login':user_login, 'user_logout':user_logout,"cartItems":cartItems,'user_staff':user_staff,'categories':categories}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'items': items, 'order': order, 'user_login':user_login, 'user_logout':user_logout,"cartItems":cartItems,'user_staff':user_staff,"categories":categories}
    return render(request, 'html/delivery.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customerName')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if not all([customer_name, mobile, city, address]):
            return HttpResponse("Vui lòng điền đầy đủ thông tin.", status=400)

        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        shipping_address = ShippingAddress(
            User=customer,
            order=order,
            address=address,
            city=city,
            state=city,  # Giả sử state = city nếu không có trường state trong form
            mobile=mobile
        )
        shipping_address.save()

        # Đặt thuộc tính complete của order thành True
        order.complete = True
        order.save()
        
        return redirect('payment')  # Thay đổi theo URL thực tế của bạn

    return render(request, 'html/delivery.html')

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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    ## sap xep gia
    sort_option = request.GET.get('sort', 'gia')
    if sort_option == 'asc':
        product = Product.objects.all().order_by('price')
    elif sort_option == 'desc':
        product = Product.objects.all().order_by('-price')
    else:
        product = Product.objects.all()
    ## phan trang
    page = request.GET.get('page')
    page = page or 1
    paginator = Paginator(product, 10)  # hiện số lượng sản phẩm
    paged_products = paginator.get_page(page)
    page_obj = product.count()
    categories = Category.objects.filter(is_sub=False)
    context = {'categories': categories,'product': paged_products, 'page_obj': page_obj,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    
    #####
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    
    context = {'categories': categories,'products':products,'active_category':active_category,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category','')
    searched = None
    keys = None
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)

    context = {"searched":searched, "keys":keys, "categories": categories, 'active_category':active_category,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff }
    
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    product = Product.objects.all()
    categories = Category.objects.filter(is_sub=False)
    context = {'product': product,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories}
    return render(request, 'html/event.html', context)
# trang liên hệ
def contactus(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    success_message = ""
    error_message = ""
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
            name,   # Chủ đề email
            message,                  # Nội dung email
            settings.EMAIL_HOST_USER, # Từ email của hệ thống
            [email],
            fail_silently=False
        )
        success_message = "Bạn đã gửi thành công"
    categories = Category.objects.filter(is_sub=False)
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories,'success_message': success_message, 'error_message': error_message}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories}
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
        if request.user.is_staff:
            user_staff = "show"
        else:
            user_staff = "hidden"
    else:
        items = []
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'user_staff':user_staff,'categories':categories}
    return render(request, 'html/location.html', context)
# trang đăng ký
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to the home page or wherever you want
    else:
        form = UserCreationForm()
    return render(request, 'html/register.html', {'form': form})
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

def create_product(request):
    if request.user.is_staff:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
        form = ProductForm()
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
        categories = Category.objects.filter(is_sub=False)
        context = {"form":form,'user_login':user_login, 'user_logout':user_logout,'cartItems':cartItems,'categories':categories}
        return render(request,'html/create_product.html',context)
    else:
        return redirect('home')

@login_required
def user(request):
    return render(request, 'html/User.html', {'user': request.user})

