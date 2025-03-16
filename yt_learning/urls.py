from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Root URL for landing page
    path('categories/', views.categories_page, name='categories_page'),  # Categories page
    path('videos/<int:category_id>/', views.videos_by_category, name='videos_by_category'),
    path('compiler/', views.Compilers_view, name='compiler'),
]