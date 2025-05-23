from django.contrib import admin
from userauths.models import User , ContactUs , Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ['username' , 'email' , 'bio']

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name' , 'email' , 'phone' , 'subject' , 'date']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name'  , 'phone' , 'verified' , 'date']



admin.site.register(User , UserAdmin)
admin.site.register(ContactUs , ContactUsAdmin)
admin.site.register(Profile , ProfileAdmin)