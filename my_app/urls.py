from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.get_my_app,name='home'),
    path('detail/',views.detail, name='detail'),
    path('cart/',views.cart, name='cart'),
    path('mypham/',views.product_mypham, name='mypham'),
    path('event/',views.event, name='event'),
]