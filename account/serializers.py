from django.db.models import fields
from .models import *

from rest_framework import fields, serializers



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

