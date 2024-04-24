from django.db import models

Role = [
        ('ADMIN','admin'),
        ('USER','user'),
 ]
Answer_Type = [
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
 ]

class user(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    role = models.CharField(max_length=15, choices=Role)
    password = models.CharField(max_length=20,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    scalp_image = models.ImageField(upload_to='scalp_image/')
    is_question_submitted = models.BooleanField(default=False)
    hair_health = models.IntegerField(default=0)
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
    
class questions(models.Model):
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class choice(models.Model):
    question = models.ForeignKey(questions,on_delete=models.CASCADE)
    choice = models.CharField(max_length=250) 
    type = models.CharField(max_length=2, choices=Answer_Type)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
class user_questinare(models.Model):
    question = models.ForeignKey(questions,on_delete=models.CASCADE)
    answer = models.ForeignKey(choice,on_delete=models.CASCADE) 
    user =  models.ForeignKey(user,on_delete=models.CASCADE) 
    earned_percent = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)      
    
