# from sys import modules
from django.db import  models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
# from django.template.defaultfilters import first, truncatechars
# from django.utils import tree


class UserManager(BaseUserManager):
    def create_user(self, username,first_name, email, password=None, **other_fields):

        if username is None:
            raise TypeError ('Users should have a username')
        if email is None:
            raise TypeError ('Users should have a Email')
        
        user = self.model(username=username, email=self.normalize_email(email),first_name=first_name,**other_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, username,first_name, email, password=None, **other_fields):
        
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff = true.'

            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser= True.'
            )

        if password is None:
            raise TypeError ('password should not be none')
         
        user = self.create_user(username,first_name, email, password, **other_fields)
        return user

AUTH_PROVIDERS={'facebook':'facebook', 'google':'google','twitter':'twitter','email':'email'}


class User(AbstractBaseUser, PermissionsMixin):
    
    username=  models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name= models.CharField(max_length=225, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider=models.CharField(max_length=250,null=True,blank=True,default='email')


    

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username', 'first_name']

    objects = UserManager()

    def __str__(self):
        return self.email

        
    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
     
    def token(self):
        return ''
