from django.urls import path
from . import views

urlpatterns = [
    path('problems_list/', views.problem_list_view, name='problems_list'),  # List of problems
    path('problems/<int:problem_id>/', views.problem_detail_view, name='problems_detail'),  # Specific problem
    #path('run-code/', views.run_code, name='run_code'),  # Code execution endpoint
]