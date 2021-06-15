from django.shortcuts import render
from django.template import response

# Create your views here.

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from account.models import User

from .models import *
from product.models import *
from .serializers import *
from rest_framework.decorators import api_view, permission_classes,authentication_classes


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def addToCart(request):

    user=request.user
    if request.method=='GET':
        carts= Cart.objects.filter(user=user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)



    if request.method=='POST':  
        try:
            product_id= request.data['id']
            product_obj=Product.objects.get(id=product_id)
            cart= Cart.objects.filter(user=user).filter(isComplete=False).filter(product=product_obj).first()
            if cart:
                print(cart)
                print('old cart')
                cart.quantity+=1
                cart.save()
            else:
                print('New cart is Created')
                Cart.objects.create(user=user, product=product_obj, quantity=1)
            
            carts= Cart.objects.filter(user=user).all()
            serializer= CartSerializer(carts, many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error':'Product DoesNotExist'}) 

    return Response({'message':'Something wrong'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addQuantity(request):
    user = request.user
    cart_id = request.data['id']
    quantity=request.data['quantity']
    try:
        cart = Cart.objects.get(pk=cart_id)
        cart.quantity+=quantity
        cart.save()
        return Response({'message':"added successfully"})
    except:
        return Response({'message':"false"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deleteCart(request):

    cart_id = request.data['id']
    try:
        cart_obj=Cart.objects.get(id=cart_id)
        cart_obj.delete()

        response_msg={'error':False}

    except:
        response_msg={'error':True}
    return Response(response_msg)


   

    




    



