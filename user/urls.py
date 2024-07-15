"""traya_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . views import * 

urlpatterns = [
    path('',Login.as_view(),name='login'),
    path('register', Register.as_view(), name='register'),
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('product',Product.as_view(),name='product'),
    path('add-to-cart',Add_to_Cart.as_view(),name='add-to-cart'),
    path('add-to-order',Add_to_Order.as_view(),name='add-to-order'),
    path('add-scalp-image',Add_Scalp_Image.as_view(),name='add-scalp-image'),
    path('remove-product',Remove_From_Cart.as_view(),name='remove-product'),
    path('diet-plan',DietPlan.as_view(),name='diet-plan'),
    path('report',Report.as_view(),name='report'),
    path('all-product',AllProducts.as_view(),name='all-products'),
    path('logout',Logout.as_view(),name='logout'),
    path('take-hair-test',TakeHairTest.as_view(),name='take-hair-test'),
    
    path('checkout', checkout, name='checkout'),
    path('payment_success', payment_success, name='payment_success'),
    path('payment_cancel', payment_cancel, name='payment_cancel'),
]
