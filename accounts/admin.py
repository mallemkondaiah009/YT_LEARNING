from django.contrib import admin
from .models import UserStreak
from django.contrib.auth.models import User

# class UserInfo(admin.ModelAdmin):
#     list_display = ('username', 'email','password')
# admin.site.register(UserRegistrations, UserInfo)

class UserStreakInfo(admin.ModelAdmin):
    list_display = ('user', 'streak_count','last_visit','longest_streak')
admin.site.register(UserStreak, UserStreakInfo)