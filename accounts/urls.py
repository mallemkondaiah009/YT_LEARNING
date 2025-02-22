from django.urls import path
from . import views

urlpatterns = [

    path('register/', views.Register_View, name='register'),
    path('login/', views.Login_View, name='login'),
    path('logout/', views.Logout_View, name='logout'),
    path('profile/', views.Profile_View, name='profile'),
]