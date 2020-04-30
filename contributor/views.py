from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'contributor/dashboard.html')

def current_projects(request):
    return render(request, 'contributor/current_projects.html')