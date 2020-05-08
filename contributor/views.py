from django.shortcuts import render, redirect

import pyrebase
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

    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("contributors").child(local_id).child("chatrooms_ids").get()
    chat_details = []
    if (chatrooms.each()):
        for chatroom in chatrooms.each():
            print(chatroom.val())
            if ('pitcher_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['pitcher_id'], 'pitchers'))

        for i, (a, b, c) in enumerate(chat_details):
            investor = firebase_database.child("users").child(c).child(b).get()
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname'), chat_details[i][2])

    print("CHAT:", chat_details)
    #########################################

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
    print(P)
    return render(request, 'contributor/dashboard.html', {'pitches': P, 'contributor_key':local_id, 'chats':chat_details})

def current_projects(request):
    return render(request, 'contributor/current_projects.html')

def chat_window(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']
    chatId = request.POST['chatId']

    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("contributors").child(local_id).child("chatrooms_ids").get()
    chat_details = []
    if (chatrooms.each()):
        for chatroom in chatrooms.each():
            print(chatroom.val())
            if ('pitcher_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['pitcher_id'], 'pitchers'))

        for i, (a, b, c) in enumerate(chat_details):
            investor = firebase_database.child("users").child(c).child(b).get()
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname'), chat_details[i][2])

    print("CHAT:", chat_details)
    #########################################

    return render(request, "contributor/chat_window.html", {'chatId':chatId, 'chats':chat_details})

def delete_account(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']

    chatroom_ids = []  # for storing the chatroom ids
    pitcher_to_pitch_ids = []  # ['pitcher_id','pitch_id']

    # fetching related chatrooms ids of the contributor
    chatrooms = firebase_database.child("users").child("contributors").child(local_id).child("chatrooms_ids").get()
    if chatrooms.each():
        for chatroom in chatrooms.each():
            chatroom_ids.append(chatroom.val()['key'])

    # removing the related chatrooms
    for chatroom in chatroom_ids:
        firebase_database.child("users").child("chatrooms").child(chatroom).remove()

    # fetching pitch ids contributor is interested in
    interested_pitches = firebase_database.child("users").child("contributors").child(local_id).child("interested_pitches").get()
    if interested_pitches.each():
        for pitch in interested_pitches.each():
            l = []
            l.append(pitch.val()['pitcher_id'])
            l.append(pitch.val()['pitch_id'])
            pitcher_to_pitch_ids.append(l)

    # for deleting in the users/pitches
    for pitcher in pitcher_to_pitch_ids:
        contributors = firebase_database.child("users").child("pitches").child(pitcher[0]).child(pitcher[1]).child("contributors").get()
        if contributors.each():
            for contributor in contributors.each():
                if contributor.val()['contributor_id'] == local_id:
                    firebase_database.child("users").child("pitches").child(pitcher[0]).child(pitcher[1]).child("contributors").child(contributor.key()).remove()

    # removing contributors from pitchers
    for entry in pitcher_to_pitch_ids:
        contributors_in_pitchers = firebase_database.child("users").child("pitchers").child(entry[0]).child("interested_contributors").get()
        if contributors_in_pitchers.each():
            for contributor in contributors_in_pitchers.each():
                if contributor.val()['contributor_id'] == local_id:
                    firebase_database.child("users").child("pitchers").child(entry[0]).child("interested_contributors").child(contributor.key()).remove()

    firebase_database.child("users").child("contributors").child(local_id).remove()
    return render(request, "users/home.html")

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
        del request.session['uid']
    except:
        print("Some error while logging out!")
    return redirect('/users/home')