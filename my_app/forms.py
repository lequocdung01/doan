from django import forms
from .models import Product, MyUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['ID','category','name','price','categy','sell','image','sale']


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    username = forms.CharField(label="Username", widget=forms.TextInput)
    firstname = forms.CharField(label="Firstname", widget=forms.TextInput)
    lastname = forms.CharField(label="Lastname", widget=forms.TextInput)
    address = forms.CharField(label="Address", widget=forms.TextInput)
    phone = forms.CharField(label="Phone", widget=forms.TextInput)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(label="Gender", choices=MyUser.GENDER_CHOICES)

    class Meta:
        model = MyUser
        fields = ["email", "username", "firstname", "lastname", "address", "phone", "date_of_birth", "gender"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
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
        fields = ["email", "password", "date_of_birth", "username", "firstname", "lastname", "gender","address", "phone", "is_active", "is_admin"]

class MyUserForm(forms.ModelForm):
    gender = forms.CharField(max_length=10, widget=forms.RadioSelect(choices=MyUser.GENDER_CHOICES))
    class Meta:
        model = MyUser
        fields = ['date_of_birth', 'gender', 'address', 'phone', 'firstname', 'lastname']
        