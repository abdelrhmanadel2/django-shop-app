
from django.core.checks import messages
import product
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication

from account.models import User

from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from account.utils import Utils
from django.contrib.sites.shortcuts import get_current_site

from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *

from rest_framework.decorators import api_view, permission_classes, authentication_classes

import jwt
from django.conf import settings

# Create your views here.
@api_view(['POST'])
def register(request):
    data = request.data
    # try:
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
    data ={'email_body':email_body, 'email_subject':'Verify your email', 'email_to':user.email}
    Utils.send_email(data)



    return Response({
        "user": serializer.data,
        "Token": str(token)
    })

    # except:
    #     message = {'message': 'User with this email already exists'}
    #     return Response(message, status=status.HTTP_400_BAD_REQUEST)

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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    if request.method == 'GET':
        user=request.user

        data=[]
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        for product in serializer.data:
            fab_product= Favorite.objects.filter(user=user).filter(product_id=product['id'])
           
            if fab_product:
                product['favorite']=fab_product[0].isFavorite
            else:
                product['favorite']=False
            data.append(product)
        return Response(data)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def addFavorite(request):
    user= request.user
    data = request.data['id']
    
    try:
        product= Product.objects.get(id=data)
        
        single_favorite_product= Favorite.objects.filter(user=user).filter(product=product).first()
        if single_favorite_product:
            isFav= single_favorite_product.isFavorite
            single_favorite_product.isFavorite = not isFav
            single_favorite_product.save()
        else:
            Favorite.objects.create(user=user, product=product, isFavorite=True)
        response_msg={'succes':'True'}

    except:
        response_msg= {'succes':'False'}
    
    return Response(response_msg)



@api_view(['GET','POST'])

def categoryView(request):
    if request.method=='GET':
        category=Category.objects.values_list('title',flat=True)
       

        # for cate in serializer.data:
        #     catedata= Category.objects
        return Response(category)

    if request.method=='POST':
        category_name= request.data['category_name']
        products= Product.objects.filter(category=category_name)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

@api_view(['GET','POST'])

def productComments(request, id):
    user= request.user
    product= Product.objects.get(pk=id) 
    
    if request.method=='GET':
        
        comment= Comment.objects.filter(product=product)
        serializer= CommentSerializer(comment, many=True)
        return Response(serializer.data)

        # for cate in serializer.data:
        #     catedata= Category.objects
        return Response(category)

    if request.method=='POST':
        comment_data = request.data['data']
        rate=request.data['rate']
        dd = Comment.objects.filter(product=product).filter(user=user)
        print
        if dd :
            messages={"message":"already exist"}
            
        else:
            comment= Comment.objects.create(user=user,comment=comment_data, rate=rate,product=product)
            messages={"message":"successfully created"}
        return Response(messages)

@api_view(['POST'])
@permission_classes([IsAuthenticated]) 

def likeComment(request):
    comment_id=request.data['id']
    user = request.user
    comment= Comment.objects.get(id=comment_id)
    try:
        like= Like.objects.filter(comment=comment)
        if like:
            print(comment)
            if request.user in comment.likes.user.all():
                comment.likes.user.remove(request.user)
                mesage={"message":"Succesfully remove like"}
            
               
                
            else:
                comment.likes.user.add(request.user)
                mesage={"message":"Succesfully like"}

                try:
                    comment.dislikes.user.remove(request.user)
                except:
                    print('noting')
            return Response(mesage)
        else:
            Like.objects.create(comment=comment)
            comment.likes.user.add(request.user)


            return Response({"message":"new like created"})
    except Like.DoesNotExist:
        return Response({'error':'Like does not exist'})


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 

def dislikedComment(request):
    comment_id=request.data['id']
    user = request.user
    comment= Comment.objects.get(id=comment_id)
    try:
        dislike= Dislike.objects.filter(comment=comment)
        if dislike:
            print(comment)
            if request.user in comment.dislikes.user.all():
                comment.dislikes.user.remove(request.user)
                mesage={"message":"Succesfully remove dislike"}
            
               
                
            else:
                comment.dislikes.user.add(request.user)
                mesage={"message":"Succesfully dislike"}

                try:
                    comment.likes.user.remove(request.user)
                except:
                    print('noting')
            return Response(mesage)
        else:
            Dislike.objects.create(comment=comment)
            comment.dislikes.user.add(request.user)


            return Response({"message":"new dislike created"})
    except Like.DoesNotExist:
        return Response({'error':'dislike does not exist'})

