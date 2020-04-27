from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from register.models import UserRegistration
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,'login.html',{'name':'Sid'})


def pitcher(request):
    return render(request,'pitcher.html')


def investor(request):
    return render(request,'investor.html')


def contributor(request):
    return render(request, 'contributor.html')


def verify(request):
    email = request.POST["email"]
    password = request.POST['password']
    role = request.POST['role']

    user = UserRegistration.objects.filter(email=email)
    user_values = user.values()

    if user.count() != 0 and user_values[0]['role'] == role:
        if(password == user_values[0]['password']):
            if role == "pitcher":
                return redirect('pitcher')
            elif role == "contributor":
                return redirect('contributor')
            else:
                return redirect('investor')
        else:
            return redirect('/')
    else:
        messages.info(request,"Invalid credentials")
        return redirect('/')
