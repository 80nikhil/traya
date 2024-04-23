from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from . models import *

class Login(TemplateView):
    template_name = 'login.html'
    model_name = user
    
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name)   
    
    def post(self,request,*args, **kwargs):
        try: 
            user_obj = self.model_name.objects.get(contact_no=request.POST.get('contact_no'),password=request.POST.get('password'),role='ADMIN')
            return redirect('/web_admin/dashboard') 
        except self.model_name.DoesNotExist: 
            return render(request,self.template_name)     


class Dashboard(TemplateView):
    template_name = 'dashboard.html'
    
    def get(self,request,*args, **kwargs):
        return render(request,self.template_name) 