from django.db import models
from accounts.models import UserRegistrations

class Bashalu(models.Model):
    lang_name = models.CharField(max_length=100)
    code = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.lang_name



class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='category_icons/', null=True)

    def __str__(self):
        return self.name
    
class Videos(models.Model):
    title = models.CharField(max_length=100)
    bhashalu = models.ForeignKey(Bashalu, on_delete=models.CASCADE,null=True)
    yt_video_url = models.URLField(null = True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    embed_code = models.TextField()
    

    def __str__(self):
        return self.title
    

class save_watch_later(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegistrations, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.video.title
    

class Language(models.Model):
    lang_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

    