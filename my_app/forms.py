from django import forms
from .models import Product
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import UserProfile
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['ID', 'category', 'name', 'price', 'categy', 'sell', 'image', 'sale']
        widgets = {
            'ID': forms.NumberInput(attrs={'class': 'input'}),
            'category': forms.Select(attrs={'class': 'input'}),
            'name': forms.TextInput(attrs={'class': 'input'}),
            'price': forms.NumberInput(attrs={'class': 'input'}),
            'categy': forms.TextInput(attrs={'class': 'input'}),
            'sell': forms.NumberInput(attrs={'class': 'input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'input'}),
            'sale': forms.NumberInput(attrs={'class': 'input'}),
        }

        
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'address', 'phone', 'birth_date', 'profile_picture']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),  # Thêm widget cho hình ảnh
        }