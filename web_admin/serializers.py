from . models import *   
from rest_framework import serializers

class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = '__all__'        
        
class question_serializer(serializers.ModelSerializer):
    class Meta:
        model = questions
        fields = '__all__' 

class package_serializer(serializers.ModelSerializer):
    class Meta:
        model = package
        fields = '__all__'         

class category_serializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = '__all__'      
        
class diet_plan_serializer(serializers.ModelSerializer):
    class Meta:
        model = diet_plan
        fields = '__all__'                   
                       