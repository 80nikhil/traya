from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from rest_framework.views import APIView
from . serializers import * 
from . models import *

class Login(TemplateView):
    template_name = 'login.html'
    model_name = user
    
    def get(self,request,*args, **kwargs):
        try:
            request.session['admin_id']
            return redirect('/web_admin/dashboard') 
        except KeyError as e:
           return render(request,self.template_name)    
    
    def post(self,request,*args, **kwargs):
        try: 
            user_obj = self.model_name.objects.get(contact_no=request.POST.get('contact_no'),password=request.POST.get('password'),role='ADMIN')
            request.session['admin_id'] = user_obj.id 
            request.session['name'] = user_obj.name 
            return redirect('/web_admin/dashboard') 
        except self.model_name.DoesNotExist: 
            return render(request,self.template_name)     


class Dashboard(TemplateView):
    template_name = 'dashboard.html'
    
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name)
    
class AddProduct(APIView):
    template_name = 'add_product.html'
    model = product
    
    def get(self,request,*args, **kwargs):
        list = self.model.objects.all()
        context={'list':list}
        return render(request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        serializer = product_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)    
        return redirect('/web_admin/add-product') 
    
class AllUsers(APIView):
    template_name = 'all_users_list.html'
    model = user
    
    def get(self,request,*args, **kwargs):
        list = self.model.objects.all()
        context={'list':list}
        return render(request,self.template_name,context) 

class AddQuestions(APIView):
    template_name = 'add_question.html'
    model = questions 
    
    def get(self,request,*args, **kwargs):
        list = self.model.objects.all()
        context={'list':list}
        return render(request,self.template_name,context)    
    
    def post(self,request,*args, **kwargs):
        serializer = question_serializer(data=request.data)
        if serializer.is_valid():
            question_obj = serializer.save()
            dic={}
            dic['1'] = request.POST.get('choice_1')
            dic['2'] = request.POST.get('choice_2')
            dic['3'] = request.POST.get('choice_3')
            dic['4'] = request.POST.get('choice_4')
            for key,value in dic.items():
                choice_obj = choice.objects.create(question=question_obj,choice=value,type=key,)
                choice_obj.save()
        else:
            print(serializer.errors)    
        return redirect('/web_admin/add-questions')  

class EditQuestion(APIView):
    template_name = 'edit_question.html'
    model = choice 
    
    def get(self,request,id,*args, **kwargs):
        list = self.model.objects.filter(question__id=id)
        print(list[0].question.question)
        context={'list':list,'question':list[0].question}
        return render(request,self.template_name,context) 
    
    def post(self,request,id,*args, **kwargs):
        my_dict = request.data
        for key,value in my_dict.items():
            try:
                int(key)
                choice_obj = self.model.objects.get(id=id)
                choice_obj.choice = value
                choice_obj.save()
            except:
                pass 
        question_obj = questions.objects.get(id=id)
        question_obj.question = request.POST.get('question') 
        question_obj.save()
        return redirect('/web_admin/add-questions')    

class DeleteQuestion(APIView):
    model = choice 
        
    def get(self,request,id,*args, **kwargs):
        related_objects = self.model.objects.filter(question__id=id)
        related_objects.delete()
        question = questions.objects.get(id=id)
        question.delete()
        return redirect('/web_admin/add-questions')
    
class AddPackage(APIView):
    model = package
    template_name = "package.html" 
    
    def get(self,request,*args, **kwargs):
        list = self.model.objects.all()
        context={'list':list}
        return render(request,self.template_name,context)
    
    def post(self,request,*args, **kwargs):
        serializer = package_serializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
        else:
            pass
        return redirect('/web_admin/add-package')    
    
class DeletePackage(APIView):
    model = package 
        
    def get(self,request,id,*args, **kwargs):
        package_objects = self.model.objects.filter(id=id)
        package_objects.delete()
        return redirect('/web_admin/add-package')    

class Logout(APIView):
    def get(self,request,*args, **kwargs):
        del request.session['admin_id']
        return redirect('/web_admin')