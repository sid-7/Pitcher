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

# Create your views here.
def dashboard(request):
    # all_pitches = AddDetails.objects.all()
    # u = AddDetails(userid=userid)
    # all_pitches = u.objects
    # for pitches in all_pitches:
    #     p.append({'title': pitches.title, 'body': pitches.description, 'tags': ['tag1', 'tag2']})
    # print(p)
    data = firebase_database.child("users").child("pitches").get()
    pitches_list = []
    P = []
    for user in data.each():
        pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
        for pitch in pitches.each():
            P.append(pitch.val())

    return render(request, 'investor/dashboard.html', {'pitches': P})

def current_projects(request):
    return render(request, 'investor/dashboard.html')

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
    except:
        print("Some error while logging out!")
    return redirect('/user/home')