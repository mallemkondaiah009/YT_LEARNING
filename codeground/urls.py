from django.urls import path
from .views import CodeReels_View

urlpatterns = [
    path('code-reels/', CodeReels_View, name='code-reels'),
]