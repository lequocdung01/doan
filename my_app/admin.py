from django.contrib import admin
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# UserAdmin là một lớp con của django.contrib.auth.admin.ModelAdmin được cung cấp sẵn để quản lý hiển thị
# Chỉnh sửa thông tin người dùng trong trang quản trị Django.

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
# admin.site.register(Review)
# admin.site.register(User)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'comment', 'rate', 'created_at')  

admin.site.register(Review, ReviewAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_order', 'complete', 'transaction_id')

admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'quantity', 'date_added')

admin.site.register(OrderItem, OrderItemAdmin)

class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'User', 'order', 'name', 'address', 'city', 'state', 'mobile', 'date_added')

admin.site.register(ShippingAddress, ShippingAddressAdmin)
