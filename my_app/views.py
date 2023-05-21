from django.shortcuts import render

# Create your views here.
def get_my_app(request):
    context = {}
    return render(request,'home.html',context)

def detail(request):
    context={}
    return render(request,'html/detail_product.html',context)

def cart(request):
    context={}
    return render(request, 'html/cart.html', context)