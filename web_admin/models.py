from django.db import models

Role = [
        ('ADMIN','admin'),
        ('USER','user'),
 ]

class user(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    role = models.CharField(max_length=15, choices=Role)
    password = models.CharField(max_length=20,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class product(models.Model):
    name = models.CharField(max_length=150)    
    description = models.TextField()
    amount = models.IntegerField(default=0)
    image = models.ImageField(upload_to='product_image/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
