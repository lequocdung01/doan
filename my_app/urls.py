from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_my_app,name='home'),
    path('detail/',views.detail, name='detail'),
    path('cart/',views.cart, name='cart'),
    path('mypham/',views.product_mypham, name='mypham'),
    path('event/',views.event, name='event'),
    path('contactus/',views.contactus, name='contactus'),
    path('regestermember/',views.regestermember, name='regestermember'),
    path('memberkhuyenmai/',views.memberkhuyenmai, name='memberkhuyenmai'),
    path('introduce/',views.introduce, name='introduce'),
    path('TuyenDung/',views.TuyenDung, name='TuyenDung'),
    path('location/',views.location, name='location'),
    path('form/',views.form, name='form'),
    path('product/',views.product, name='product'),
]