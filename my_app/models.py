from django.contrib import admin
from django.db import models
# AbstractBaseUser là một lớp cơ sở trừu tượng được cung cấp sẵn để tạo ra mô hình người dùng tùy chỉnh. 
# Khi bạn muốn tạo một hệ thống người dùng riêng biệt và không sử dụng mô hình người dùng mặc định của Django, 
# bạn có thể kế thừa AbstractBaseUser để tạo ra mô hình người dùng theo ý muốn.
from django.contrib.auth.models import User

# Create your models here.

# tạo class product dùng để chứa các sản phẩm của website
class Product(models.Model):
    ID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    categy = models.CharField(max_length=200,null=True)
    sell = models.IntegerField()
    image = models.ImageField(null=True,blank=True)
    sale = models.IntegerField(null=True)
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete = models.CASCADE, related_name='sub_categories',null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
class UserAdmin(admin.ModelAdmin):
    # Cấu hình hiển thị thông tin user trong trang admin
    list_display = ['username', 'email', 'first_name', 'last_name']

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=False)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200,null=False)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default = False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_item(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address =models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


