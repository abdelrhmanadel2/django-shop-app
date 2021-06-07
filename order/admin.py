
from django.contrib import admin
from .models import *

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'quantity']
    list_filter = ['user']


admin.site.register(Cart, CartAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Order)
