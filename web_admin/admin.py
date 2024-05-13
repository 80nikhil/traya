from django.contrib import admin
from . models import * 

admin.site.register(user)
admin.site.register(product)
admin.site.register(questions)
admin.site.register(choice)
admin.site.register(user_questinare)
admin.site.register(package)