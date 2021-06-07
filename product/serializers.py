from rest_framework import fields, serializers
from account.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import *

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
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields= ['image']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields= ['point']

class ProductSerializer(serializers.ModelSerializer):
    images= ImageSerializer(many=True,read_only=True)
    productSpecification= ProductSpecificationSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id',  'title','keywords','description','image','price','slug','category','avaragereview',
        'no_of_reviews','images','productSpecification'
    ]


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category;
        fields=['title']


class CommentSerializer(serializers.ModelSerializer):
    user= MinUserDataSerializer(many=False)
    class Meta:
        model = Comment

        fields=['id','user','comment','rate','get_total_likes', 'get_total_dislikes']
        depth=1