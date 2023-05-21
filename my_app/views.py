from django.shortcuts import render
from .models import *
# Create your views here.
def get_my_app(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request,'html/home.html',context)