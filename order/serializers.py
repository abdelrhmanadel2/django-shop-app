import product
from order.models import *
from rest_framework import serializers
from product.serializers import *

class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False,read_only=True)

    class Meta:
        model = Cart

        fields=['id','quantity','product','amount']
        depth=1
        