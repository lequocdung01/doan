from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


# UserAdmin là một lớp con của django.contrib.auth.admin.ModelAdmin được cung cấp sẵn để quản lý hiển thị
# Chỉnh sửa thông tin người dùng trong trang quản trị Django.

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(ShippingAddress)
# admin.site.register(Review)
admin.site.unregister(User)

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
    list_display = ('id', 'User', 'order', 'address', 'city', 'state', 'mobile', 'date_added')

admin.site.register(ShippingAddress, ShippingAddressAdmin)




class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )
    gender = forms.ChoiceField(choices=MyUser.GENDER_CHOICES)
    address = forms.CharField(label="Address",widget=forms.Textarea)
    phone = forms.CharField(label="Phone", widget=forms.TextInput)
    username = forms.CharField(label="Username", widget=forms.TextInput)
    class Meta:
        model = MyUser
        fields = ["email", "date_of_birth", "username", "gender","address", "phone"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ["email", "password", "date_of_birth", "username", "gender","address", "phone", "is_active", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "date_of_birth", "gender","address", "username", "phone", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["date_of_birth","gender","address", "username", "phone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2", "email", "date_of_birth","gender", "address", "phone"],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)

