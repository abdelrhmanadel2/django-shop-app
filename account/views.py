from django.core.checks import messages
from django.http import response
from django.http.response import Http404
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from account.models import User
from product.serializers import UserSerializer
from rest_framework.authtoken.models import Token


from .models import *
from .serializers import *

from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.contrib.auth.hashers import make_password


# Create your views here.
@api_view(['POST'])
def registera(request):
    data = request.data
    # try:
    serializer= RegisterSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
  
    user = UserSerializer(serializer, many=False)
    

    return Response({
    "user": user.data,
    
    })

    # except:
    #     message = {'message': 'User with this email already exists'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)