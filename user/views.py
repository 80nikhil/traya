from django.db.models import OuterRef, Subquery
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,View
from rest_framework.views import APIView
from django.contrib import messages
from . serializers import * 
from  web_admin.models import *
from . models import * 
from web_admin.models import *
from django.db.models import Q
import decimal
from django.db.models import Sum

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
                # question_list = self.model_name.objects.filter(category=user_obj.category).exclude(id__in=submitted_question).first()
                question_list = self.model_name.objects.all()
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
    template_name = 'user_cart.html'
    model_name = product   
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            cart_list = cart.objects.filter(user__id=user_id).values_list('product__id',flat=True)
            product_list = self.model_name.objects.filter(id__in=cart_list)
            actual_price = product_list.aggregate(TOTAL = Sum('actual_price'))['TOTAL']
            amount = product_list.aggregate(TOTAL = Sum('amount'))['TOTAL']
            context = {'product_list':product_list,'cart_count':get_cart_count(request)}
            context['actual_price'] = actual_price
            context['amount'] = amount
            return render(request,self.template_name,context) 
        
        except KeyError as e:
           return redirect('/user/')  
    
    def post(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            package_obj = package.objects.get(id=request.POST.get('package'))
            for prod_obj in product.objects.filter(package=package_obj):
                if cart.objects.filter(product=prod_obj,user__id=user_id).exists():
                    pass
                else:
                    cart_obj = cart.objects.create(product=prod_obj,
                                                            user=user.objects.get(id=user_id))

                    cart_obj.save()
            return redirect('/user/add-to-cart')
        
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
            return redirect('/user/take-hair-test')
        
        except KeyError as e:
           return redirect('/user/') 

class Report(View):
    model_name = user
    template_name = "report_page.html"
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            user_obj = user.objects.get(id=user_id)
            question_1 = user_questinare.objects.filter(user=user_obj,question__report_priority=1).first()
            if question_1.answer.choice == 'Stage-6':
                recovery = 0
            elif question_1.user.hair_health == 100: 
                recovery = 100
            elif question_1.user.hair_health > 75: 
                recovery = 95
            elif question_1.user.hair_health > 50: 
                recovery = 90
            elif question_1.user.hair_health > 25: 
                recovery = 85
            else:
                recovery = 75
            package_obj = package.objects.filter(min__lte=user_obj.hair_health,max__gte=user_obj.hair_health).first()
            package_obj.min = round((package_obj.actual_price - package_obj.price) / (package_obj.actual_price / 100),2)
            package_items_list = package_items.objects.filter(package=package_obj)  
            product_list = product.objects.filter(package=package_obj)  
            context = {'user':user_obj,'question_1':question_1,'recovery':recovery,'cart_count':get_cart_count(request),
                       'package':package_obj,'package_items_list':package_items_list,'product_list':product_list}
            return render(request,self.template_name,context)
        except KeyError as e:
           return redirect('/user/')     
                       
       
class Logout(APIView):
    
    def get(self,request,*args, **kwargs):
        del request.session['user_id']
        return redirect('/')   
    
    
class TakeHairTest(APIView):
    model = questions
    template_name = "take_hair_test.html"

    def get(self,request,*args, **kwargs):
        question_obj = self.model.objects.filter(is_subque=False).order_by('id')
        que_per = 0
        try: 
            user_id=request.session['user_id']
            user_obj = user.objects.get(id=request.session['user_id'])
            question_obj = question_obj.filter(Q(gender__isnull=True)|Q(gender=user_obj.gender))
            excluded_que = []
            subquery = questions.objects.filter(is_subque=True, main_que__id=OuterRef('main_que__id')).order_by('id').values('id')[:1]
            distinct_questions = questions.objects.filter(id__in=Subquery(subquery))
            for main_que_obj in distinct_questions:
                if user_questinare.objects.filter(user__id=user_id,question__main_que=main_que_obj.main_que).count() == self.model.objects.filter(is_subque=True,main_que=main_que_obj.main_que).count():
                    excluded_que.append(main_que_obj.id) 
            questionare_list = user_questinare.objects.filter(user__id=user_id,question__is_subque=False).values_list('question__id',flat=True)
            excluded_que.extend(list(questionare_list))
            try:
                que_per = (100/question_obj.count())*user_questinare.objects.filter(user__id=user_id,question__is_subque=False).count()
            except :
                pass
            if len(excluded_que)>0: 
                question_obj = question_obj.exclude(id__in=excluded_que)
        except:
            pass    
        question_obj = question_obj.first()
        category_list = category.objects.all().order_by('id')
        try:        
            if self.model.objects.filter(is_subque=True,main_que=user_obj.last_update_que).exists():
                if user_questinare.objects.get(user=user_obj,question=user_obj.last_update_que).answer.priority == False:
                    question_obj = question_obj.exclude(id=user_obj.last_update_que.id)
                elif user_questinare.objects.get(user=user_obj,question=user_obj.last_update_que).answer.priority == True:
                    user_que = user_questinare.objects.filter(user=user_obj,question__main_que=user_obj.last_update_que).values_list('question__id',flat=True)     
                    new_question_obj = self.model.objects.filter(is_subque=True,main_que=user_obj.last_update_que).exclude(id__in=list(user_que))
                    if new_question_obj.exists() >0:
                        question_obj = new_question_obj.first() 
                    else:
                        question_obj = question_obj.exclude(id=user_obj.last_update_que.id)    
        except:
            pass    
        if question_obj:
            for category_obj in category_list:
                if category_obj == question_obj.category:
                    category_obj.is_active = 'active'
                else:
                    category_obj.is_active = 'inactive'   
        choices = choice.objects.filter(question=question_obj)    
        if not question_obj:
            if user_obj.scalp_image:
                return redirect('/user/report')
            else:
                status = 'scalp'
        else:
            status = 'question'                   
        context={'que_per':round(que_per,2),'question_obj':question_obj,'category_list':category_list,'choices':choices,'status':status}
        return render(request,self.template_name,context)
   
    def post(self,request,*args, **kwargs): 
        question = self.model.objects.get(id=request.POST.get('question'))
        if question.name:
            if question.name == 'contact_no' and question.category.name == 'About You':
                try: 
                    user_obj = user.objects.get(contact_no=request.POST.get('choice'))
                    request.session['user_id'] = user_obj.id  
                    return redirect('/user/take-hair-test') 
                except user.DoesNotExist:
                    user_obj = user(contact_no=request.POST.get('choice'),role='USER',is_active=True)
                    user_obj.save()
                    user_obj = user.objects.get(contact_no=request.POST.get('choice'))
                request.session['user_id'] = user_obj.id     
            else:
                user_obj = user.objects.get(id=request.session['user_id'])
                question_name = question.name 
                choice_value = request.POST.get('choice') 
                setattr(user_obj, question_name, choice_value)
                user_obj.save() 
            user_questinare_obj = user_questinare(user=user_obj,question=question) 
            user_questinare_obj.save()
            if question.is_subque == False:
             user_obj.last_update_que = question
            user_obj.save()       
        else:
            user_obj = user.objects.get(id=request.session['user_id'])
            choice_obj= choice.objects.get(id=request.POST.get('choice'))
            que_per = 100/self.model.objects.filter(Q(gender__isnull=True)|Q(gender=user_obj.gender),is_subque=False,is_scoring_que=True).count()
            if self.model.objects.filter(is_subque=True,main_que=question).exists():
                sub_que_per = self.model.objects.filter(is_subque=True,main_que=question).count()
                hair_health = que_per/sub_que_per
                hair_health = hair_health/100
                hair_health = decimal.Decimal(hair_health)*choice_obj.score 
            else:
                hair_health = decimal.Decimal((que_per/100))*choice_obj.score  
            user_questinare_obj = user_questinare(user=user_obj,question=question,answer=choice_obj,earned_percent=hair_health) 
            user_questinare_obj = user_questinare_obj.save()
            if question.is_subque == False:
                user_obj.last_update_que = question
            if question.issue_category and choice_obj.priority == True:
                user_obj.issue_categories.add(question.issue_category)    
            user_obj.hair_health = decimal.Decimal(user_obj.hair_health) + decimal.Decimal(hair_health)         
            user_obj.save()
        return redirect('/user/take-hair-test')   
    
class DietPlan(View):
    template_name = "user_diet_plan.html"
    model_name = diet_plan
    
    def get(self,request,*args, **kwargs):
        try:
            user_id=request.session['user_id']
            user_obj = user.objects.get(id=user_id)
            diet_obj = self.model_name.objects.filter(min__lte=user_obj.hair_health,max__gte=user_obj.hair_health)
            dic_max = {}
            for issue in user_obj.issue_categories.all():
                for obj in diet_obj.filter(categories=issue):
                    if not obj.id in dic_max:
                        dic_max[obj.id] = 1
                    else:
                        dic_max[obj.id] = dic_max[obj.id] + 1
            print(dic_max) 
            max_key = max(dic_max.items(), key=lambda k: k[0])[0]
            diet_meal_obj = diet_meal_plan.objects.filter(diet_plan__id=max_key)
            diet_obj = diet_meal_obj.last().diet_plan
            context = {'diet_plan':diet_obj,'diet_meal_obj':diet_meal_obj,'cart_count':get_cart_count(request)}
            return render(request,self.template_name,context) 
        except KeyError as e:
           return redirect('/')     
             
'''--------------------------payment---------------------------'''
from django.shortcuts import HttpResponse, render
from django.conf import settings
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .utils import *
from django.conf import settings
from django.shortcuts import render
import base64

def encrypt(data, working_key):
    data_bytes = data.encode('utf-8')
    encrypted_data = base64.b64encode(data_bytes)  # Placeholder for actual encryption
    return encrypted_data.decode('utf-8')

def checkout(request):
    p_merchant_id = settings.CC_MERCHANT_ID
    current_site = 'https://fidorehealth.com/'
    p_order_id = '0001'
    p_currency = settings.CC_CURRENCY
    p_amount = '100'
    p_redirect_url = f"{current_site}/payment_success/"
    p_cancel_url = f"{current_site}/payment_cancel/"
    p_language = settings.CC_LANG

    billing_info = {
        'billing_name': 'Foo Bar',
        'billing_address': '12/Foo Bar',
        'billing_city': 'Pune',
        'billing_state': 'Maharashtra',
        'billing_zip': '411002',
        'billing_country': settings.CC_BILL_CONTRY,
        'billing_tel': '9988776655',
        'billing_email': 'foobar@domain.com',
    }

    delivery_info = {
        'delivery_name': '',
        'delivery_address': '',
        'delivery_city': '',
        'delivery_state': '',
        'delivery_zip': '',
        'delivery_country': 'India',
        'delivery_tel': '',
    }

    merchant_params = {
        'merchant_param1': '',
        'merchant_param2': '',
        'merchant_param3': '',
        'merchant_param4': '',
        'merchant_param5': '',
        'promo_code': '',
        'customer_identifier': '',
    }

    merchant_data = {
        'merchant_id': p_merchant_id,
        'order_id': p_order_id,
        'currency': p_currency,
        'amount': p_amount,
        'redirect_url': p_redirect_url,
        'cancel_url': p_cancel_url,
        'language': p_language,
        **billing_info,
        **delivery_info,
        **merchant_params,
    }

    merchant_data_str = '&'.join([f"{key}={value}" for key, value in merchant_data.items()])
    encrypted_merchant_data = encrypt(merchant_data_str, settings.CC_WORKING_KEY)

    data_dict = {
        'p_redirect_url': p_redirect_url,
        'encryption': encrypted_merchant_data,
        'access_code': settings.CC_ACCESS_CODE,
        'cc_url': settings.CC_URL,
        'p_amount': p_amount
    }

    return render(request, 'payment.html', data_dict)


@csrf_exempt
def payment_success(request):

    """
    Method to handel cc-ave payment success.
    :param request:
    :return:
    """

    response_data = request.POST

    response_chiper = response_data.get('encResp')
    payment_list = decrypt(response_chiper, settings.CC_WORKING_KEY)

    # payment success code

    return HttpResponse('DONE')


@csrf_exempt
def payment_cancel(request):

    """
    Method to handel cc-ave.
    :param request: data
    :return: status
    """

    response_data = request.POST

    response_chiper = response_data.get('encResp')
    payment_list = decrypt(response_chiper, settings.CC_WORKING_KEY)

    # payment cancel code

    return HttpResponse('Cancel')