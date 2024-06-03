from web_admin.models import *   
from rest_framework import serializers

class register_serializer(serializers.ModelSerializer):
    class Meta:
        model = user
        fields = ['name','contact_no','email','role','is_active','gender','category','profile_image']