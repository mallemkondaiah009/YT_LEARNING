from django.urls import path
from . import views

urlpatterns = [
    path('sentiment-analizer/', views.analyze_sentiment, name='analyze_sentiment'),
]