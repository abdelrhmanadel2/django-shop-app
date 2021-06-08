from account.serializers import *
from rest_framework import fields, serializers
from account.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import *

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



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= Category;
        fields=['title']


class CommentSerializer(serializers.ModelSerializer):
    user= MinUserDataSerializer(many=False)
    class Meta:
        model = Comment

        fields=['id','user','comment','rate','get_total_likes', 'get_total_dislikes','whenpublished']
        depth=1