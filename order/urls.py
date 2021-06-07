from .views import *
from account.views import *
from django.urls import path, include

urlpatterns = [
    path('carts/', addToCart,name='addtocart'),
    path('deletecart/', deleteCart, name='deleteCart')

]
