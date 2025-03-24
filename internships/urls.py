
from django.urls import path
from .views import Internships_View


urlpatterns = [
    path('internships/',Internships_View, name='internships'),
] 