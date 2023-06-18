from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_my_app,name='home'),
    path('detail/',views.detail, name='detail'),
    path('cart/',views.cart, name='cart'),
    path('delivery/',views.delivery, name='delivery'),
    path('update_item/',views.updateItem, name='update_item'),
    path('payment/',views.payment, name='payment'),
    path('category/',views.category, name='category'),
    path('event/',views.event, name='event'),
    path('contactus/',views.contactus, name='contactus'),
    path('regestermember/',views.regestermember, name='regestermember'),
    path('memberkhuyenmai/',views.memberkhuyenmai, name='memberkhuyenmai'),
    path('introduce/',views.introduce, name='introduce'),
    path('TuyenDung/',views.TuyenDung, name='TuyenDung'),
    path('location/',views.location, name='location'),
    path('register/',views.register, name='register'),
    path('product/',views.product, name='product'),
    path('search/',views.search, name='search'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutPage, name='logout'),
    path('create/',views.create_product,name='create')
]