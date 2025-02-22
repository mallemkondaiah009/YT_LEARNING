from django.contrib import admin
from .models import UserRegistrations

class UserInfo(admin.ModelAdmin):
    list_display = ('username', 'email','password')
admin.site.register(UserRegistrations, UserInfo)
