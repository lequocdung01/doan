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
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg, Count, Sum, F
from django.http import HttpResponse  # Import HttpResponse từ django.http
from django.db import IntegrityError
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.shortcuts import render
# from .forms import ContactForm
# import smtplib
# from django.db.models.functions import TruncMonth
from collections import defaultdict
# Create your views here.

# chua context chung cua cac def khac
def get_common_context(request):
    context = {}
    
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
        user_login = "hidden"
        user_logout = "show"
        user_staff = "show" if request.user.is_staff else "hidden"
        context.update({
            'user_profile': user_profile,
            'items': items,
            'order': order,
            'cartItems': cartItems,
            'user_login': user_login,
            'user_logout': user_logout,
            'user_staff': user_staff,
            'customer': customer,
        })
    else:
        order = {'get_cart_item': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_item']
        user_login = "show"
        user_logout = "hidden"
        user_staff = "hidden"
        context.update({
            'items': [],
            'order': order,
            'cartItems': cartItems,
            'user_login': user_login,
            'user_logout': user_logout,
            'user_staff': user_staff,
        })
    context['categories'] = Category.objects.filter(is_sub=False)
    return context

# trang thong ke
def sstatistics(request):
    context = get_common_context(request)

    # Lấy danh sách các tháng có đơn hàng
    orders = Order.objects.filter(complete=True).order_by('-date_order')
    monthly_stats = defaultdict(lambda: {'total_orders': 0, 'total_items': 0, 'total_amount': 0.0})
    
    # Tạo thống kê hàng tháng
    for order in orders:
        month_key = order.date_order.strftime('%Y-%m')
        monthly_stats[month_key]['total_orders'] += 1
        monthly_stats[month_key]['total_items'] += sum(item.quantity for item in order.orderitem_set.all())
        monthly_stats[month_key]['total_amount'] += order.get_cart_total

    # Nếu không có tháng nào được chọn, lấy tháng gần nhất
    selected_month = request.GET.get('month', None)
    if not selected_month:
        if monthly_stats:
            selected_month = max(monthly_stats.keys())  # Tháng gần nhất
        else:
            selected_month = timezone.now().strftime('%Y-%m')  # Tháng hiện tại nếu không có dữ liệu

    # Xác định khoảng thời gian của tháng được chọn
    selected_month_start = datetime.strptime(selected_month, '%Y-%m')
    selected_month_end = (selected_month_start.replace(day=28) + timedelta(days=4)).replace(day=1)

    # Lọc đơn hàng dựa trên tháng được chọn
    filtered_orders = Order.objects.filter(
        complete=True, 
        date_order__gte=selected_month_start, 
        date_order__lt=selected_month_end
    ).select_related('customer').prefetch_related('orderitem_set', 'shippingaddress_set')
    
    order_data = []
    
    for order in filtered_orders:
        order_items = order.orderitem_set.all()
        shipping_address = order.shippingaddress_set.first()
        items_data = []
        total_items = 0
        total_amount = 0.0
        for item in order_items:
            product = item.product
            items_data.append({
                'product_name': product.name,
                'product_image': product.ImageURL,
                'quantity': item.quantity,
                'price': item.product.price,
                'total_price': item.get_total
            })
            total_items += item.quantity
            total_amount += item.get_total
        
        order_data.append({
            'order_id': order.id,
            'customer_username': order.customer.username,
            'date_order': order.date_order,
            'items': items_data,
            'total_amount': order.get_cart_total,
            'name': shipping_address.name if shipping_address else '',
            'address': shipping_address.address if shipping_address else '',
            'city': shipping_address.city if shipping_address else '',
            'state': shipping_address.state if shipping_address else '',
            'mobile': shipping_address.mobile if shipping_address else '',
        })

    categories = Category.objects.filter(is_sub=False)
    context.update({
        'categories': categories,
        'orders': order_data,
        'monthly_stats': sorted(monthly_stats.items()),
        'user': request.user,
        'selected_month': selected_month,
        'product': product,
        
    })
    return render(request, 'html/sstatistics.html', context)

# trang lịch sử mua hàng
@login_required
def history(request):
    context = get_common_context(request)

    # Add specific logic for history view
    customer = context['customer']
    completed_orders = Order.objects.filter(customer=customer, complete=True)
    order_items = OrderItem.objects.filter(order__in=completed_orders).select_related('product')

    purchased_items = []
    for item in order_items:
        shipping_address = ShippingAddress.objects.filter(order=item.order).first()
        purchased_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'total_price': item.get_total,
            'date_added': shipping_address.date_added if shipping_address else None,
        })

    context.update({
        'purchased_items': purchased_items,
    })
    
    return render(request, 'html/history.html', context)

# trang chu
def get_my_app(request):
    context = get_common_context(request)

    # Add specific logic for home view
    product = Product.objects.all()
    page = request.GET.get('page') or 1
    paginator = Paginator(product, 6)
    paged_products = paginator.get_page(page)
    page_obj = product.count()

    context.update({
        'product': product,
        'paged_products': paged_products,
        'page_obj': page_obj,
    })
    
    return render(request, 'html/home.html', context)

# chi tiết sản phẩm
def detail(request):
    context = get_common_context(request)

    prod_id = request.GET.get('id', '')
    product = get_object_or_404(Product, ID=prod_id)

    # Lấy giá trị trung bình của rate từ các đánh giá của sản phẩm
    avg_rate = Review.objects.filter(product=product).aggregate(Avg('rate'))['rate__avg'] or 0
    reviews = Review.objects.filter(product=product)

    context.update({
        'product': product,
        'products': Product.objects.filter(ID=prod_id),
        'avg_rate': avg_rate,
        'reviews': reviews,
    })
    
    return render(request, 'html/detail.html', context)

def review(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        comment = request.GET.get('comment')
        rate = request.GET.get('star')
        
        # Kiểm tra xem tất cả các giá trị cần thiết có được truyền vào không
        if not prod_id or not comment or not rate:
            return HttpResponse('Missing required parameters', status=400)
        
        # Lấy sản phẩm, nếu không tồn tại sẽ trả về 404
        product = get_object_or_404(Product, ID=prod_id)
        
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not request.user.is_authenticated:
            return HttpResponse('User not authenticated', status=403)
        
        # Lấy ngày hiện tại
        created_at = timezone.now()
        user = request.user
        
        # Tạo và lưu review mới
        Review.objects.create(user=user, product=product, comment=comment, rate=rate, created_at=created_at)
        
        # Sử dụng reverse để xây dựng URL của trang detail và truyền prod_id qua kwargs
        detail_url = reverse('detail')
        return redirect(detail_url + f'?id={prod_id}')
    else:
        return HttpResponse('Invalid request method', status=405)


# 
def cart(request):
    context = get_common_context(request)
    return render(request, 'html/cart.html', context)

#Thanh toan
def delivery(request):
    context = get_common_context(request)
    return render(request, 'html/delivery.html', context)

@login_required
@login_required
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        address = request.POST.get('address')

        if not all([name, mobile, city, address]):
            return JsonResponse({'success': False, 'message': 'Vui lòng điền đầy đủ thông tin.'}, status=400)

        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        shipping_address = ShippingAddress(
            User=customer,
            order=order,
            name=name,
            address=address,
            city=city,
            state=city,  # Giả sử state = city nếu không có trường state trong form
            mobile=mobile
        )
        shipping_address.save()

        order.complete = True
        order.save()
        
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Phương thức yêu cầu không hợp lệ.'}, status=405)

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
    context = get_common_context(request)
    return render(request, 'html/payment.html', context)


# trang sản phẩm
def product(request):
    context = get_common_context(request)

    sort_option = request.GET.get('sort', 'gia')
    
    if sort_option == 'asc':
        products = Product.objects.all().order_by('price')
    elif sort_option == 'desc':
        products = Product.objects.all().order_by('-price')
    elif sort_option == 'new':
        products = Product.objects.all().order_by('-ID')
    elif sort_option == 'selling':
        products = Product.objects.annotate(total_sold=Sum('orderitem__quantity')).order_by('-total_sold')
    else:
        products = Product.objects.all()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)
    paged_products = paginator.get_page(page)
    
    context.update({
        'product': paged_products,
    })
    
    return render(request, 'html/product.html', context)

# Tran san pham
def category(request):
    context = get_common_context(request)
    
    active_category = request.GET.get('category', '')
    sort_option = request.GET.get('sort', 'gia')
    
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
        
        if sort_option == 'asc':
            products = products.order_by('price')
        elif sort_option == 'desc':
            products = products.order_by('-price')
        elif sort_option == 'new':
            products = products.order_by('-ID')
        elif sort_option == 'selling':
            products = products.annotate(total_sold=Sum('orderitem__quantity')).order_by('-total_sold')

        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        paged_products = paginator.get_page(page)

        context.update({
            'products': paged_products,
            'active_category': active_category,
            'sort_option': sort_option
        })

    return render(request, 'html/category.html', context)



# trang tìm kiếm
def search(request):
    context = get_common_context(request)

    active_category = request.GET.get('category', '')
    searched = None
    keys = None
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains=searched)

    context.update({
        "searched": searched,
        "keys": keys,
        'active_category': active_category,
    })
    
    return render(request, 'html/search.html', context)


# trang sự kiện
def event(request):
    context = get_common_context(request)
    context['product'] = Product.objects.all()
    return render(request, 'html/event.html', context)

# trang liên hệ
def contactus(request):
    context = get_common_context(request)
    
    success_message = ""
    error_message = ""
    
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        try:
            send_mail(
                name,  # Subject
                message,  # Message
                settings.EMAIL_HOST_USER,  # From email
                [email],  # To email
                fail_silently=False,
            )
            success_message = "Bạn đã gửi thành công"
        except BadHeaderError:
            error_message = "Invalid header found."
        except Exception as e:
            error_message = str(e)

    context.update({
        'success_message': success_message,
        'error_message': error_message,
    })
    
    return render(request, 'html/contactus.html', context)

# trang đăng ký thành viên 
def regestermember(request):
    context = get_common_context(request)
    return render(request, 'html/regestermember.html', context)

# trang khuyến mãi
def memberkhuyenmai(request):
    context = get_common_context(request)
    return render(request, 'html/memberkhuyenmai.html', context)

# trang giới thiệu
def introduce(request):
    context = get_common_context(request)
    return render(request, 'html/introduce.html', context)

# trang tuyển dụng
def TuyenDung(request):
    context = get_common_context(request)
    return render(request, 'html/TuyenDung.html', context)

# trang địa chỉ
def location(request):
    context = get_common_context(request)
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
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Tên đăng nhập không tồn tại!')
            else:
                messages.error(request, 'Mật khẩu không đúng!')
    return render(request, 'html/loginPage.html')

# trang dang xuat
def logoutPage(request):
    logout(request)
    messages.success(request=request,message='Bạn đã đăng xuất thành công!')
    return redirect('login')

# trang them san pham moi
def create_product(request):
    if request.user.is_staff:
        context = get_common_context(request)
        form = ProductForm()
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
        
        context.update({
            "form": form,
        })
        
        return render(request, 'html/create_product.html', context)
    else:
        return redirect('home')

# trang thong tin nguoi dung
@login_required
def user(request):
    context = get_common_context(request)
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user')
    else:
        form = UserProfileForm(instance=user_profile)
    context.update({
        'form': form, 
        'user': request.user,
    })
    return render(request, 'html/User.html', context)
    
# trang quan ly san pham
def Product_Manager(request):
    context = get_common_context(request)
    
    if request.method == 'POST' and 'delete_product' in request.POST:
        product_id = request.POST.get('product_id')
        product_to_delete = get_object_or_404(Product, pk=product_id)
        product_to_delete.delete()
        return redirect('management')

    context.update({
        'product': Product.objects.all(),
        'count_product': Product.objects.count(),
    })
    
    return render(request, 'html/Product_Management.html', context)

# trang sua thong tin san pham
def edit_product(request):
    product_id = request.GET.get('id')
    product = get_object_or_404(Product, ID=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('management')  # Redirect to the product management page or any other page
    else:
        form = ProductForm(instance=product)
    return render(request, 'html/edit_product.html', {'form': form})