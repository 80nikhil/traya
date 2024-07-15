from django.db import models
from web_admin.models import * 

Order_Status= [
    ('ORDERED','Ordered'),
    ('SHIPPED','Shiipped'),
    ('DELIEVERED','Delievered'),
]

class cart(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class order(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    user = models.ForeignKey(user,on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Order_Status,default='ORDERED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class transaction_history(models.Model):    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
