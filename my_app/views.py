from django.shortcuts import render

# Create your views here.
def get_my_app(request):
    return render(request,'html/home.html')