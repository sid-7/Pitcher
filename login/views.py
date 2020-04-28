from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from register.models import UserRegistration
from django.contrib import messages
import pyrebase
#first upgrade setuptools (1.pip install --upgrade setuptools 2. pip install pyrebase)
# Create your views here.

config = {
"apiKey": "AIzaSyBTlSwWe6lD6NLi8OrDPe49qWIllNgttMI",
    "authDomain": "pitcher-275100.firebaseapp.com",
    "databaseURL": "https://pitcher-275100.firebaseio.com",
    "projectId": "pitcher-275100",
    "storageBucket": "pitcher-275100.appspot.com",
    "messagingSenderId": "1008306122255",
    "appId": "1:1008306122255:web:58559788fa73c384fcbd7a",
    "measurementId": "G-GPL016L81F"
}
firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def login_page_with_firebase(request):
    return render(request,"login_with_firebase.html")

def firebase_login(request):
    email = request.POST["email"]
    password = request.POST["password"]

    user = auth.sign_in_with_email_and_password(email,password)
    print(user)

    return render(request,"pitcher.html")


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
