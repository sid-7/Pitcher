from django.shortcuts import render, redirect

import datetime
import pyrebase
########################  firebase authentication  ##################################
config = {
  "apiKey": "AIzaSyBTlSwWe6lD6NLi8OrDPe49qWIllNgttMI",
  "authDomain": "pitcher-275100.firebaseapp.com",
  "databaseURL": "https://pitcher-275100.firebaseio.com",
  "storageBucket": "pitcher-275100.appspot.com",
  "serviceAccount": "serviceAccountCredentials.json"
}
firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth()
firebase_database = firebase.database()
##########################################################################################
def home(request):
    return render(request, 'users/home.html')

def login(request):
    if(len(request.POST)==0 or request.POST.get('email')==''):
        return render(request, 'users/login.html')
    else:
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        # user = UserRegistration.objects.filter(email=email)
        # # user = auth.authenticate(username=username,password=password)
        # user_values = user.values()
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        account_info = firebase_auth.get_account_info(user['idToken'])  # to get account info of the user
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        print(user, account_info)
        #########################
        #### to add role checking
        #########################

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

def signup(request):
    if(len(request.POST)==0 or request.POST.get('email')==''):
        return render(request, 'users/signup.html')
    else:
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        #user = UserRegistration(first_name=first_name, last_name=last_name, password=password, email=email, role=role)
        #user.save()
        print(email, password)
        firebase_auth.create_user_with_email_and_password(email, password)
        print("user created")

        user = firebase_auth.sign_in_with_email_and_password(email, password)

        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        account_info = firebase_auth.get_account_info(str(session_id))  # to get account info of the user

        local_id = account_info['users'][0]['localId']
        date = str(datetime.date.today())
        data = {'firstname': firstname, 'lastname': lastname, 'email': email, 'role': role, 'date_joined': date}
        firebase_database.child("users").child(role + "s").child(local_id).set(data)

        if (role == 'pitcher'):
            request.session['email'] = email
            request.session['role'] = role
            return redirect("/pitcher/dashboard")
        elif (role == 'investor'):
            request.session['email'] = email
            request.session['role'] = role
            return redirect("/investor/dashboard")
        elif (role == 'contributor'):
            request.session['email'] = email
            request.session['role'] = role
            return redirect("/contributor/dashboard")
        else:
            del request.sesssion['email']
            del request.sesssion['role']
            del request.sesssion['uid']
            return render(request, "users/home.html", {"message":"User registration successful!"})

def reset_password(request):
    if(len(request.POST)>1):
        email = request.POST.get("email")
        try:
            firebase_auth.send_password_reset_email(email)
        except:
            print("error occured")
        message = "email has been sent to you email address"
        return redirect('/users/home', {message})
    else:
        return render(request, "users/reset_password.html")

def about(request):
    pass

def contact(request):
    pass