from django.shortcuts import render, redirect
from users.models import UserRegistration
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def login(request):
    if(len(request.POST)==0 or request.POST.get('email')==''):
        return render(request, 'users/login.html')
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        user = UserRegistration.objects.filter(email=email)
        # user = auth.authenticate(username=username,password=password)
        user_values = user.values()

        if user.count() != 0 and user_values[0]['role'] == role:
            if (password == user_values[0]['password']):
                print(role)
                if(role=='pitcher'):
                    request.session['email'] = email
                    request.session['role'] = role
                    return redirect("/pitcher/dashboard")
                elif(role=='investor'):
                    request.session['email'] = email
                    request.session['role'] = role
                    return redirect("/investor/dashboard")
                elif(role=='contributor'):
                    request.session['email'] = email
                    request.session['role'] = role
                    return redirect("/contributor/dashboard")
                else:
                    return redirect("/user/home", {'message':'Role error'})
            else:
                return render(request, 'users/login.html', {'message':'Invalid login credentials.'})
        else:
            return render(request, 'users/login.html', {'message':'Invalid login credentials.'})

def signup(request):
    if(len(request.POST)==0 or request.POST.get('email')==''):
        return render(request, 'users/signup.html')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        user = UserRegistration(first_name=first_name, last_name=last_name, password=password, email=email, role=role)
        user.save()
        print("user created")
        return render(request, "users/home.html", {"message":"User registration successful!"})

def about(request):
    pass

def contact(request):
    pass