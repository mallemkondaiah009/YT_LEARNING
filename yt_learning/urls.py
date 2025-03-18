
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  # Root URL for landing page
    path('categories/', views.categories_page, name='categories_page'),  # Categories page
    path('videos/<str:category_name>/', views.videos_by_category, name='videos_by_category'),
    path('codeground/', views.Code_Ground_view, name='codeground'),
    path('compilers/', views.Compilers_view, name='compilers'),
]