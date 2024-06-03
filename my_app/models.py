from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core import validators
# Create your models here.

# tạo class product dùng để chứa các sản phẩm của website
class Category(models.Model):
    sub_category = models.ForeignKey('self',on_delete=models.CASCADE, related_name="sub_categories",null=True,blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200,unique=True)

    def __str__(self):
        return self.name
class Product(models.Model):
    ID = models.IntegerField(primary_key=True)
    category = models.ManyToManyField(Category,related_name="product")
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    categy = models.CharField(max_length=200,null=True)
    sell = models.IntegerField()
    image = models.ImageField(null=True,blank=True)
    sale = models.IntegerField(null=True)
    star_rating = models.FloatField(default=0,null=True)  # Thêm trường star_rating
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class UserAdmin(admin.ModelAdmin):
    # Cấu hình hiển thị thông tin user trong trang admin
    list_display = ['username', 'email', 'first_name', 'last_name']
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
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
    User = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, null=True)
    address =models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey(Product, models.CASCADE)
    comment = models.TextField(max_length=250)
    rate = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']





