
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




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    if request.method == 'GET':
        user=request.user
        if user:
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
        else:
          return Response({"message":"Not valid token"},status=status.HTTP_400_BAD_REQUEST)

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

# GetProductComments
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated]) 
def productComments(request, id):
    user= request.user
    product= Product.objects.get(pk=id) 
    
    if request.method=='GET':
        
        comments= Comment.objects.filter(product=product)
        serializer= CommentSerializer(comments, many=True)
        data=[]

        # User like or dislike on comment Status

        for comment in serializer.data:
            productComment= Comment.objects.get(pk=comment['id'])
            print(productComment)
            try:      
                if request.user in productComment.likes.user.all():
                    comment['like']= True
                    comment['dislike']=False
                elif request.user in productComment.dislikes.user.all():
                    comment['like']=False
                    comment['dislike']=True
                else:
                    comment['like']=False
                    comment['dislike']=False
                data.append(comment)
            except:
                comment['like']=False
                comment['dislike']=False
                data.append(comment)

        return Response(data)
        


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

