
from django.db.models.fields import EmailField
from account.helpers import send_otp_to_email
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from account.models import User

from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from account.utils import Utils
from django.contrib.sites.shortcuts import get_current_site

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from .models import *
from .serializers import *

from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes

import jwt
from django.conf import settings
from rest_framework.views import APIView
from  rest_framework.throttling import AnonRateThrottle


@api_view(['POST'])
def register(request):
    data = request.data
    try:
        user = User.objects.create_user(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=data['password'])
        token = AccessToken.for_user(user)
        serializer = UserSerializer(user, many=False)
        current_site= get_current_site(request).domain
        relativeLink=reverse('verify-email')

        absurl ='http://'+current_site+relativeLink+"?token="+str(token)
        email_body= 'Hi'+user.username+' Use link below to verify your email\n '+ absurl
        data ={'email_body':email_body, 'email_subject':'Verify your email ', 'email_to':user.email}
        Utils.send_email(data)



        return Response({
            "user": serializer.data,
            "Token": str(token)
        })
    except:
        return Response ({'message':"user with this email already exist"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def verifyEmail(request):
    token= request.GET.get('token')
  
    print('token='+token)
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
        print('payload 1 ' + str(payload))
        user = User.objects.get(id=payload['user_id'])
        if not user.is_verified:
            user.is_verified=True
            user.save()
        
        return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as e:
        return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as e:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@throttle_classes([AnonRateThrottle])
def changePassword(request):   
    token= request.GET.get('token')
    data= request.data

    try: 
        # We can not expire any refresh or access token so for logout or expire
        # we need to add token to blacklist so with it can not accessible 

        refresh_token=RefreshToken(token)
        refresh_token.blacklist()
    except:
        return Response ({"message":"Link is expired"},status=status.HTTP_400_BAD_REQUEST)
  
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
       
        user = User.objects.get(id=payload['user_id'])
        user.set_password(data['new_password'])
        user.save()
        
        return Response({'message': 'password successfully reset'}, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError as e:
        return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as e:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    try:
        serializer = LoginSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token = AccessToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            "Token": str(token),

        })

    except:
        message = {'message': 'Unable to log in with provided credentials'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([TokenAuthentication])
def getUserProfile(request):
    try:
        user = request.user
        serializer = UserSerializer(user, many=False)
        # token, created = Token.objects.get_or_create(user=user)
        token = AccessToken.for_user(user)
        return Response({
        "user": serializer.data,
        "Token":str(token)

        })
    except:
        messages= {"message":"Invalid Token"}
        return Response(messages ,status= status.HTTP_400_BAD_REQUEST)
   

@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([TokenAuthentication])
def getUser(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


class ForgetPassword(APIView):

    def post(self,request):
        try:
            data = request.data
            user_obj=User.objects.get(email=data['email'])
            otp=data['otp']

            if user_obj.otp==otp:
                token=RefreshToken.for_user(user_obj)
                current_site= get_current_site(request).domain
                relativeLink=reverse('change-password')

                reset_link='http://'+current_site+relativeLink+"?token="+str(token)
                user_obj.otp=5555
                user_obj.save()
               

                return Response({'reset_link':reset_link},status=status.HTTP_200_OK)
            return Response({'message':'wrong code'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
        return Response({'error':'Something Wrong'}, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self, request):

        try:
            data = request.data 
            user_obj=User.objects.get(email=data['email'])
            if not User.objects.filter(email= data['email']).exists():
                return Response({'message':'No user found'},status=status.HTTP_400_BAD_REQUEST)
            send_status =send_otp_to_email(data['email'],user_obj)
            if send_status:

                validation_code=user_obj.otp
                print(validation_code)

                data={'email_body':str(validation_code),'email_subject':'Use this code for Password reset','email_to':user_obj.email}
                Utils.send_email(data)
                return Response({'message':'New otp send', },status=status.HTTP_201_CREATED)
            else: 
                return Response({'message':'Try after few Seconds'}, status= status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
        return Response({'error':'Something Wrong'}, status=status.HTTP_400_BAD_REQUEST)
      


