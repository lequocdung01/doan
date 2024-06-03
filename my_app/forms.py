from django import forms
from .models import Product
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['ID','category','name','price','categy','sell','image','sale']


# class MyUserForm(forms.ModelForm):
#     gender = forms.CharField(max_length=10, widget=forms.RadioSelect(choices=MyUser.GENDER_CHOICES))
#     class Meta:
#         model = MyUser
#         fields = ['date_of_birth', 'gender', 'address', 'phone', 'firstname', 'lastname']
        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)