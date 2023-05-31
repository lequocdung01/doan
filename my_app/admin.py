from django.contrib import admin
from .models import *
# UserAdmin là một lớp con của django.contrib.auth.admin.ModelAdmin được cung cấp sẵn để quản lý hiển thị
# Chỉnh sửa thông tin người dùng trong trang quản trị Django.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Đăng ký UserAdmin cho mô hình User mặc định
admin.site.unregister(User)
# Register your models here.
admin.site.register(Product)
admin.site.register(category)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)


# 
class AccountAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'username', 'first_name', 'last_name')   # Các trường có gắn link dẫn đến trang detail
    readonly_fields = ('last_login', 'date_joined')     # Chỉ cho phép đọc
    ordering = ('-date_joined',)     # Sắp xếp theo chiều ngược

    # Bắt buộc phải khai báo
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)