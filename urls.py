from django.contrib import admin
from django.urls import path
from .  import views

urlpatterns = [
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.registerform, name='register'),
    path('', views.loginform, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.UserPage, name='user'),

]
