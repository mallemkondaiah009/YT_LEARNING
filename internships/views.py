from django.shortcuts import render

# Create your views here.
def Internships_View(request):
    return render(request, 'internships/internships.html')