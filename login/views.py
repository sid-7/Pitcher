from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from register.models import UserRegistration
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request,'login.html',{'name':'Sid'})

def homepage(request):
    return render(request,'user.html')

def user(request):
    email = request.POST["email"]
    password = request.POST['password']
    role = request.POST['role']

    user = UserRegistration.objects.filter(email=email)
    #user = auth.authenticate(username=username,password=password)
    user_values = user.values()
    print(user_values[0])

    if user.count() != 0 and user_values[0]['role'] == role:
        if(password == user_values[0]['password']):
            return redirect('homepage')
        else:
            return redirect('/')
    else:
        messages.info(request,"Invalid credentials")
        return redirect('/')
