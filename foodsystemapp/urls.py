from django.contrib import admin
from django.urls import path
from foodsystemapp import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('resturantsignup/', views.resturantsignup, name='resturantsignup'),
    path('customersignup/', views.customersignup, name='customersignup'),
    path('login/', views.login, name='login'),
    path('customerhome/', views.customerhome, name='customerhome'),
    path('resturanthome/', views.resturanthome, name='resturanthome'),
    path('orderfood/', views.orderfood, name='orderfood'),
    path('checkoutdetails/', views.checkoutdetails, name='checkoutdetails'),
    path('displayalert/', views.displayalert, name='displayalert'),
    path('custorderdetails/', views.custorderdetails, name='custorderdetails'),
    path('fooditemsadded/', views.fooditemsadded, name='fooditemsadded'),
    path('viewitems/', views.viewitems, name='viewitems'),
    path('hotelspecific/', views.hotelspecific, name='hotelspecific'),


]
