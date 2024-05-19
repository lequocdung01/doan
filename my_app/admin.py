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
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.unregister(User)

class UserAdmin(BaseUserAdmin):
    
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id", "username","email", "date_of_birth", "gender","address", "phone", "firstname", "lastname", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["username", "password", "email","gender"]}),
        ("Personal info", {"fields": ["date_of_birth","address", "phone", "firstname", "lastname"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2", "email", "date_of_birth","gender", "address", "phone", "firstname", "lastname"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["id"]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

