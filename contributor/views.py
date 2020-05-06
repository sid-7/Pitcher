from django.shortcuts import render, redirect
from django.shortcuts import render, redirect


import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, storage
config = {
  "apiKey": "AIzaSyBTlSwWe6lD6NLi8OrDPe49qWIllNgttMI",
  "authDomain": "pitcher-275100.firebaseapp.com",
  "databaseURL": "https://pitcher-275100.firebaseio.com",
  "storageBucket": "pitcher-275100.appspot.com",
  "serviceAccount": "serviceAccountCredentials.json"
}
cred=credentials.Certificate('serviceAccountCredentials.json')
firebase = pyrebase.initialize_app(config)

firebase_auth = firebase.auth()
firebase_database = firebase.database()
firebase_storage = firebase.storage()
########################################################################

def dashboard(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
    except:
        return redirect("users/home", {'message':'Error while authenticating. Please login again!'})
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']

    data = firebase_database.child("users").child("pitches").get()
    if(firebase_database.child("users").child("investors").child(local_id).child('interested_pitches').get().val()==None):
        interested_pitches = []
    else:
        interested_pitches = [x['pitch_id'] for x in (dict(firebase_database.child("users").child("investors").child(local_id).child('interested_pitches').get().val()).values())]

    print(interested_pitches)

    P = []
    for user in data.each():
        pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
        for pitch in pitches.each():
            p = pitch.val()
            d = {'pitch_key': pitch.key(), "pitcher_key": user.key(), 'title': p.get('title'),
                 'body': p.get('description'), 'date': p.get('date_created'),
                 'status': p.get('status'), "conrtibutors": p.get('contributors'), "investors": p.get('investors')}
            d['file'] = "https://storage.googleapis.com/unique-490/Friends.mp4"  # p.get('filename')
            d['tags'] = p.get('tags')
            d['gist'] = p.get('gist')
            d['interested'] = True if (d['pitch_key'] in interested_pitches) else False
            P.append(d)

    # chatrooms = firebase_database.child("users").child("contributors").child(local_id).child("chatrooms_ids").get()
    # chatroom_ids = []
    # for chatroom in chatrooms.each():
    #     chatroom_key = chatroom.val()['key']
    #     chatroom_ids.append(chatroom_key)

    # print(chatroom_ids)
    print(P)
    return render(request, 'contributor/dashboard.html', {'pitches': P, 'contributor_key':local_id})

def current_projects(request):
    return render(request, 'contributor/current_projects.html')

def to_chatroom(request):
    pass

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
        del request.session['uid']
    except:
        print("Some error while logging out!")
    return redirect('/users/home')