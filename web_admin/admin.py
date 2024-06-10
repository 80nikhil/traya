from django.contrib import admin
from . models import * 

admin.site.register(user)
admin.site.register(product)
class questionsAdmin(admin.ModelAdmin):
    model = questions
    list_display = ['id', 'question','get_category']
    def get_category(self, obj):
        return obj.category.name
admin.site.register(questions, questionsAdmin)
class choiceAdmin(admin.ModelAdmin):
    model = choice
    list_display = ['id','choice','get_question','score']
    def get_question(self, obj):
        return obj.question.question
admin.site.register(choice,choiceAdmin)
class user_questinareAdmin(admin.ModelAdmin):
    model = user_questinare
    list_display = ['id','get_contact_no','get_question','get_choice','earned_percent' ]
    def get_contact_no(self, obj):
        return obj.user.contact_no
    def get_question(self, obj):
        return obj.question.question
    def get_choice(self, obj):
        try:  
            return obj.answer.choice
        except:
            return ""
admin.site.register(user_questinare, user_questinareAdmin)
admin.site.register(package)
class categoryAdmin(admin.ModelAdmin):
    model = category
    list_display = ['id','name']
admin.site.register(category,categoryAdmin)
admin.site.register(diet_plan)
class package_itemsAdmin(admin.ModelAdmin):
    model = package_items
    list_display = ['get_package','name']
    def get_package(self, obj):
        return obj.user.contact_no
admin.site.register(package_items)

class issue_categoryAdmin(admin.ModelAdmin):
    model = issue_category
    list_display = ['name']
admin.site.register(issue_category,issue_categoryAdmin)    
    