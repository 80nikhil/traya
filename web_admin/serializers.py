from . models import *   
from rest_framework import serializers

class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'        