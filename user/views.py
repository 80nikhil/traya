from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,View
from rest_framework.views import APIView
from django.contrib import messages
from . serializers import * 
from  web_admin.models import *
from . models import * 
from web_admin.models import *

def get_cart_count(request):
    user_id=request.session['user_id']
    user_obj = user.objects.get(id=user_id)
    return cart.objects.filter(user=user_obj).count()

class Register(View):
    template_name = 'register_user.html'
    serializer = register_serializer
    model_name = user
    
    def get(self,request,*args, **kwargs):
        try:
            request.session['user_id']
            return redirect('/user/dashboard') 
        except KeyError as e:
           category_list = category.objects.all()
           context = {'category_list':category_list}
           return render(request,self.template_name,context)  
    
    def post(self,request,*args, **kwargs):
        try:
            self.model_name.objects.get(contact_no=request.POST.get('contact_no'))
            messages.error(request,'User already exist with contact no')
            return redirect('/user/register')
        except user.DoesNotExist:    
            serializer = self.serializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                messages.success(request,'Register Succesfully')
                return redirect('/user/')
            else:
                messages.error(request,'Registration Failed')
                return redirect('/user/register')   
       
class Login(TemplateView):
    template_name = 'login_user.html'
    model_name = user
    
    def get(self,request,*args, **kwargs):
        try:
            request.session['user_id']
            return redirect('/user/dashboard') 
        except KeyError as e:
           return render(request,self.template_name)    
    
    def post(self,request,*args, **kwargs):
        try: 
            user_obj = self.model_name.objects.get(contact_no=request.POST.get('contact_no'))
            request.session['user_id'] = user_obj.id 
            request.session['name'] = user_obj.name 
            return redirect('/user/dashboard') 
        except self.model_name.DoesNotExist: 
            return render(request,self.template_name)  

def get_eficiency_per(type):
    if type == '1' :
        return 25
    elif type == '2' :
        return 50
    elif type == '3' :
        return 75
    elif type == '4' :
        return 100
    
            
class Dashboard(TemplateView):
    template_name = 'user_dashboard.html'
    model_name = questions   
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            print(user_id)
            user_obj = user.objects.get(id=user_id)
            if user_obj.is_question_submitted and user_obj.scalp_image:
                list = user_questinare.objects.filter(user=user_obj)
                product_list = product.objects.filter(min__lte=user_obj.hair_health,max__gte=user_obj.hair_health)
                package_list = package.objects.filter(min__lte=user_obj.hair_health,max__gte=user_obj.hair_health)
                diet_list = diet_plan.objects.filter(min__lte=user_obj.hair_health,max__gte=user_obj.hair_health)
                context = {'scalp_image':True,'answer_list':list,'user':user_obj,'product_list':product_list,'package_list':package_list,
                           'diet_list':diet_list,'cart_count':get_cart_count(request)}
            elif  user_obj.is_question_submitted :
                context = {'scalp_image':False}
            else:    
                submitted_question=user_questinare.objects.filter(user__id=user_id).values_list('question__id',flat=True)
                question_list = self.model_name.objects.filter(category=user_obj.category).exclude(id__in=submitted_question).first()
                choice_list = choice.objects.filter(question=question_list)
                context = {'list':question_list,'choices':choice_list,'cart_count':get_cart_count(request)}
            return render(request,self.template_name,context)
        except KeyError as e:
           return redirect('/user/')  
       
    def post(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            question_per = 100/len(questions.objects.all())
            choice_obj = choice.objects.get(id=request.POST.get('choice'))
            health_per = (question_per/100)*(int(get_eficiency_per(choice_obj.type)))
            user_obj = user.objects.get(id=user_id)
            answer = user_questinare.objects.create( question=choice_obj.question,
                                                    answer=choice_obj,
                                                    user=user_obj,
                                                    earned_percent=health_per)
            answer.save()
            user_obj.hair_health = user_obj.hair_health + health_per
            if len(self.model_name.objects.exclude(id__in=user_questinare.objects.filter(user__id=user_id).values_list('question__id',flat=True))) == 0:
                user_obj.is_question_submitted = True 
            user_obj.save()    
            return redirect('/user/dashboard') 
        except KeyError as e:
           return redirect('/user/')   
    
class Product(TemplateView):
    template_name = 'product.html'
    model_name = product   
    
    def get(self,request,*args, **kwargs):
        product_list = self.model_name.objects.all()
        context = {'list':product_list,'cart_count':get_cart_count(request)}
        return render(request,self.template_name,context) 
    
class Add_to_Cart(TemplateView):
    template_name = 'cart.html'
    model_name = cart   
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            product_list = self.model_name.objects.filter(user__id=user_id)
            context = {'list':product_list,'cart_count':get_cart_count(request)}
            return render(request,self.template_name,context) 
        
        except KeyError as e:
           return redirect('/user/')  
    
    def post(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            cart_obj = self.model_name.objects.create(product=product.objects.get(id=request.POST.get('product')),
                                                      user=user.objects.get(id=user_id))

            cart_obj.save()
            return redirect('/user/product')
        
        except KeyError as e:
           return redirect('/user/')     
       
class Add_to_Order(TemplateView):
    model_name = order
    template_name = "order.html"
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            list = self.model_name.objects.filter(user__id=user_id)
            context = {'list':list,'cart_count':get_cart_count(request)}
            return render(request,self.template_name,context)
        except KeyError as e:
           return redirect('/user/') 
    
    def post(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            cart_obj = self.model_name.objects.create(product=product.objects.get(id=request.POST.get('product')),
                                                      user=user.objects.get(id=user_id))

            cart_obj.save()
            return redirect('/user/product')
        
        except KeyError as e:
           return redirect('/user/')             
    
class Remove_From_Cart(TemplateView):    
     model_name = cart
     
     def post(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            cart_obj = self.model_name.objects.get(id=request.POST.get('product'))
            cart_obj.delete()
            return redirect('/user/add-to-cart')
        
        except KeyError as e:
           return redirect('/user/') 
       
class Add_Scalp_Image(TemplateView):    
     model_name = user
     
     def post(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            print(user_id)
            user_obj = self.model_name.objects.get(id=user_id)
            user_obj.scalp_image = request.FILES.get('image')
            user_obj.save()
            return redirect('/user/dashboard')
        
        except KeyError as e:
           return redirect('/user/') 

class Report(View):
    model_name = user
    template_name = "reports.html"
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            user_obj = user.objects.get(id=user_id)
            questions = user_questinare.objects.filter(user=user_obj)
            context = {'user':user_obj,'questions':questions,'cart_count':get_cart_count(request)}
            return render(request,self.template_name,context)
        except KeyError as e:
           return redirect('/user/')     
                       
       
class Logout(APIView):
    
    def get(self,request,*args, **kwargs):
        del request.session['user_id']
        return redirect('/user')               