from social_auth import serializers
from social_auth.serializers import FacebookSerializer, GoogleSocialAuthSerializer
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response


from rest_framework.decorators import api_view

# Create your views here.


@api_view(['POST'])
def googleSocialAuth(request):
       
        
   """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

   serializer = GoogleSocialAuthSerializer(data=request.data)
   serializer.is_valid(raise_exception=True)
   data = ((serializer.validated_data)['auth_token'])
   return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def facebookSocialAuth(request):

     serializer= FacebookSerializer(data=request.data)
     serializer.is_valid(raise_exception=True)
     data=((serializer.validated_data)['auth_token'])
     return Response(data, status=status.HTTP_200_OK)
       