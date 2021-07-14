from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# Register your models here.

class UserAdminConfig(BaseUserAdmin):

    search_fields=['email', 'username',]
    list_filter=('email','username','first_name',)
    ordering=('created_at',)
    list_display =['password','email','username','first_name','auth_provider', 'is_active','is_staff','is_verified']

    fieldsets =(
        (None,{'fields':('email','username','first_name','otp')}),
           
        ('Permissions',{'fields':('is_staff','is_active', 'is_superuser','is_verified')}),
       
    )
    
    add_fieldsets = (
        ('Personal Data',{
            'classes':('wide',),
            'fields':('email','username','first_name','password1','password2',),   
        }),
         ('Permissions',{'fields':('is_staff','is_active','is_superuser')})
    )
    


admin.site.register(User, UserAdminConfig)

