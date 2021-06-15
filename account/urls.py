from inspect import getcomments
from order.views import addQuantity
from .views import *
from account.views import *
from django.urls import path, include




urlpatterns = [
  
    path('user/profile/', getUserProfile, name="user_profile"),
    path('register/', register, name='register'),
    path('users/', getUser, name='users'),
    path('login/', login, name='login'),
    path('verify-email', verifyEmail, name='verify-email'),
]
