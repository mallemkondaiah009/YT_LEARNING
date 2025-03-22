from django.urls import path,include
from . import views

urlpatterns = [
    
    path('register/', views.Register_View, name='register'),
    path('login/', views.Login_View, name='login'),
    path('logout/', views.Logout_View, name='logout'),
    path('profile/', views.Profile_View, name='profile'),
    path('register_category/', views.Register_Category_View, name='register_category'),
    path('login_category/', views.Login_Category_View, name='login_category'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
]