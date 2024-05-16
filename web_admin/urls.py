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
    path('dashboard',Dashboard.as_view(),name='dashboard'),
    path('add-product',AddProduct.as_view(),name='add-product'),
    path('all-users',AllUsers.as_view(),name='all-users'),
    path('add-questions',AddQuestions.as_view(),name='add-questions'),
    path('edit-question/<int:id>',EditQuestion.as_view(),name='edit-questions'),
    path('edit-question',EditQuestion.as_view(),name='edit-questions'),
    path('add-package',AddPackage.as_view(),name='add-package'),
    path('delete-package/<int:id>',DeletePackage.as_view(),name='delete-package'),
    path('delete-question/<int:id>',DeleteQuestion.as_view(),name='delete-questions'),
    # path('add-category',AddCategory.as_view(),name='add-category'),
    path('logout',Logout.as_view(),name='logout'),
]
