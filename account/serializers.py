from django.db.models import fields
from rest_framework.decorators import authentication_classes
from .models import *

from rest_framework import fields, serializers

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True,max_length=68, min_length=6 )

    class Meta:
        model= User
        fields= ['email', 'username','password', 'first_name']
    
    def validate(self, data):
        # email= data.get('email', '')
        # username = data.get('username', '')


        # if  username is None:
        #     raise serializers.validationError(
        #         'the user name must not be null'
        #     )
        return data
    def create(self, validated_data):   
        return User.objects.create_user(**validated_data)  


class MinUserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','username']

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    isStaff = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username',  'email', 'name', 'isAdmin', 'isStaff', ]

    def get_isAdmin(self, obj):
        isAdmin = obj.is_superuser
        return isAdmin

    def get_username(self, obj):
        username = obj.username
        return username

    def get_isStaff(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email
        return name
class LoginSerializers(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        max_length=128,
        write_only=True
    )

    def validate(self, data):
        username = data.get('email')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data

