# Django
from django.contrib import admin
# Project
from .models import Profile

class AccountsAdmin(admin.ModelAdmin):
     list_display = ['user', 'city']

     class Meta:
         model = Profile
    
# Admin Register
admin.site.register(Profile, AccountsAdmin)