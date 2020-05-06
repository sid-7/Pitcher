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
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']

    data = firebase_database.child("users").child("pitches").get()
    interested_pitches = [x['pitch_id'] for x in (dict(firebase_database.child("users").child("investors").child(local_id).child('interested_pitches').get().val()).values())]

    print(interested_pitches)

    P = []
    for user in data.each():
        pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
        for pitch in pitches.each():
            p = pitch.val()

            d = {'pitch_key': pitch.key(), "pitcher_key":user.key(), 'title': p.get('title'), 'body': p.get('description'),'date': p.get('date_created'),'status': p.get('status'), "conrtibutors": p.get('contributors'), "investors": p.get('investors')}
            d['file'] = "https://storage.googleapis.com/unique-490/Friends.mp4"#p.get('filename')
            d['tags'] = p.get('tags')
            d['gist'] = p.get('gist')
            d['interested'] = True if(d['pitch_key'] in interested_pitches) else False
            P.append(d)
    print(P)
    return render(request, 'investor/dashboard.html', {'pitches': P, 'investor_key':local_id})

def current_projects(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']

    data = firebase_database.child("users").child("pitches").get()
    interested_pitches = [x['pitch_id'] for x in (dict(firebase_database.child("users").child("investors").child(local_id).child('interested_pitches').get().val()).values())]
    P = []
    for user in data.each():
        pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
        for pitch in pitches.each():
            p = pitch.val()
            d = {'pitch_key': pitch.key(), "pitcher_key":user.key(), 'title': p.get('title'), 'body': p.get('description'),'date': p.get('date_created'),
                 'status': p.get('status'), "conrtibutors": p.get('contributors'), "investors": p.get('investors')}
            d['file'] = "https://storage.googleapis.com/unique-490/Friends.mp4"#p.get('filename')
            d['tags'] = p.get('tags')
            d['gist'] = p.get('gist')
            if(d['pitch_key'] in interested_pitches):
                d['interested'] = True
                P.append(d)

    return render(request, 'investor/dashboard.html', {'pitches': P, 'investor_key':local_id})

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
        del request.session['uid']
    except:
        print("Some error while logging out!")
    return redirect('/users/home')