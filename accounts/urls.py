from django.urls import path,include
from . import views

urlpatterns = [
    
    path('register/', views.Register_View, name='register'),
    path('login/', views.Login_View, name='login'),
    path('logout/', views.Logout_View, name='logout'),
    path('profile/', views.Profile_View, name='profile'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]