from typing import Any
from django.db import models
# AbstractBaseUser là một lớp cơ sở trừu tượng được cung cấp sẵn để tạo ra mô hình người dùng tùy chỉnh. 
# Khi bạn muốn tạo một hệ thống người dùng riêng biệt và không sử dụng mô hình người dùng mặc định của Django, 
# bạn có thể kế thừa AbstractBaseUser để tạo ra mô hình người dùng theo ý muốn.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

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
class category(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# tạo mô phỏng người dùng
class MyAccountManager(AbstractBaseUser):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('User name is required')

        # Tạo đối tượng user mới
        user = self.model(
            email=self.normalize_email(email=email),    # Chuyển email về dạng bình thường
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user
    
# tạo class tài khoản 
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'    # Trường quyêt định khi đăng nhập
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']    # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin    # Admin có tất cả quyền trong hệ thống

    def has_module_perms(self, add_label):
        return True
    


