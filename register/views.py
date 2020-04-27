from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from register.models import  UserRegistration
# Create your views here.

def register(request):
    return render(request,'register.html')

def add_to_database(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    role = request.POST['role']

    user = UserRegistration(first_name=first_name,last_name=last_name,password=password,email=email,role=role)
    user.save()
    print(user)
    # user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    # user.save()
    print("user created")
    return redirect('/')