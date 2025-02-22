from django.contrib import admin
from .models import Category, Videos, save_watch_later

# Register your models here.
admin.site.register(Category)
admin.site.register(Videos)

class save_watch_laterAdmin(admin.ModelAdmin):
    list_display = ('video', 'user', 'date')
admin.site.register(save_watch_later, save_watch_laterAdmin)
