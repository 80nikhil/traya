from django.db import models
from web_admin.models import * 

class cart(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
