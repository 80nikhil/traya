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
Gender= [
    ('MALE','Male'),
    ('FEMALE','Female')
]


class category(models.Model):
    name =models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class issue_category(models.Model):
    name = models.CharField(max_length=100)  
    
    def __str__(self):
        return self.name 
    
class questions(models.Model):
    question = models.TextField()
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    gender = models.CharField(max_length=15, choices=Gender,blank=True,null=True)
    is_subque = models.BooleanField(default=False)
    main_que = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True)
    is_scoring_que = models.BooleanField(default=True)
    name = models.CharField(max_length=20,null=True,blank=True)
    report_priority = models.IntegerField(null=True,blank=True)
    issue_category = models.ForeignKey(issue_category,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class user(models.Model):
    name = models.CharField(max_length=50)
    contact_no = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    email = models.CharField(max_length=30)
    role = models.CharField(max_length=15, choices=Role)
    password = models.CharField(max_length=20,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    gender = models.CharField(max_length=15, choices=Gender)
    age = models.IntegerField(default=0,null=True,blank=True)
    scalp_image = models.ImageField(upload_to='scalp_image/',null=True,blank=True)
    is_question_submitted = models.BooleanField(default=False)
    hair_health = models.FloatField(default=0)
    issue_categories = models.ManyToManyField(issue_category,null=True,blank=True)
    last_update_que = models.ForeignKey(questions,on_delete=models.CASCADE,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class choice(models.Model):
    question = models.ForeignKey(questions,on_delete=models.CASCADE)
    choice = models.CharField(max_length=250) 
    des_img = models.ImageField(upload_to='choice_desc_img/',null=True,blank=True) 
    score = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class user_questinare(models.Model):
    question = models.ForeignKey(questions,on_delete=models.CASCADE)
    answer = models.ForeignKey(choice,on_delete=models.CASCADE,null=True,blank=True) 
    user =  models.ForeignKey(user,on_delete=models.CASCADE) 
    earned_percent = models.DecimalField(default=0,decimal_places=2,max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    
class diet_plan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    diet_doc = models.FileField(upload_to='diet_doc/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   
    
class package(models.Model):
    name = models.CharField(max_length=150) 
    duration = models.IntegerField(default=0)
    actual_price = models.FloatField(default=0)
    price = models.FloatField(default=0.0)
    is_active = models.BooleanField()
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)     
    
class package_items(models.Model):
    package = models.ForeignKey(package,on_delete=models.CASCADE)
    name = models.CharField(max_length=150) 
    actual_price = models.FloatField(default=0)
    price = models.FloatField(default=0.0)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class product(models.Model):
    name = models.CharField(max_length=150)    
    amount =  models.FloatField(default=0)
    actual_price =  models.FloatField(default=0)
    package = models.ForeignKey(package,on_delete=models.CASCADE)
    short_desc = models.TextField()
    desc = models.TextField()
    image = models.ImageField(upload_to='product_image/')
    schedule = models.TextField()
    categories = models.ManyToManyField(issue_category, related_name='issues') 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

   
         
