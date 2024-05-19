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
    address =models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, firstname, lastname, date_of_birth, gender, address, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth, gender, address, phone and password.
        """
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            id=self.model.objects.last().id + 1 if self.model.objects.last() else 1,
            email=self.normalize_email(email),
            username=username,
            firstname=firstname,
            lastname=lastname,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone=phone,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, firstname, lastname, date_of_birth, gender, address, phone, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username,
            password=password,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone=phone,
            firstname=firstname,
            lastname=lastname,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    username = models.CharField(max_length=25, unique=True)
    date_of_birth = models.DateField(null=True)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=10, null=True, validators=[validators.RegexValidator(r'^[0-9]*$', 'Phone number must be numeric')])
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    objects = MyUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    