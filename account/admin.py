from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin

 # Unregister default Outstandingtokan admin to permit delete user 

class NewOutstandingTokenAdmin(OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(models.OutstandingToken)
admin.site.register(models.OutstandingToken, NewOutstandingTokenAdmin)

# User admin model.

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

