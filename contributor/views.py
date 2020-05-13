from django.shortcuts import render, redirect

import pyrebase
config = {
 
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

    #print(interested_pitches)

    #########  get chatrooms  ############
    print("contributor LOCALID:",local_id)
    chatrooms = firebase_database.child("users").child("contributors").child(local_id).child("chatrooms_ids").get()
    chat_details = []
    print(chatrooms)
    if chatrooms.each():
        for chatroom in chatrooms.each():
            print("_>",chatroom.val())
            if ('pitcher_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['pitcher_id'], 'pitchers'))

        for i, (a, b, c) in enumerate(chat_details):
            investor = firebase_database.child("users").child(c).child(b).get()
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname'), chat_details[i][2])
    #########################################
    P = []
    if (data.each()):
        for user in data.each():
            pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
            for pitch in pitches.each():
                p = pitch.val()
                d = firebase_database.child("users/pitches/" + local_id + "/" + pitch.key() + "/" + "contributors").get().val()
                contributors = '0'
                if (d):
                    contributors = len([x['contributor_id'] for x in dict(d).values()])
                d = firebase_database.child("users/pitches/" + local_id + "/" + pitch.key() + "/" + "investors").get().val()
                investors = '0'
                if (d):
                    investors = len([x['investor_id'] for x in dict(d).values()])
                d = {'pitch_key': pitch.key(), 'title': p.get('title', "No Title Found"), 'pitcher_key': user.key(),
                     'body': p.get('description', "No Description Found"),
                     'date': p.get('date_created'), 'status': p.get('status', "active"), 'file': p.get("file"),
                     "conrtibutors": contributors, "investors": investors, 'gist':p.get('gist')}

                d['interested'] = True if (d['pitch_key'] in interested_pitches) else False
                P.append(d)
    return render(request, 'contributor/dashboard.html', {'pitches': P, 'contributor_key':local_id, 'chats':chat_details})

def current_projects(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except Exception as e:
        return logout(request)

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
    data = firebase_database.child("users").child("pitches").get()
    try:
        interested_pitches = [x['pitch_id'] for x in (dict(
            firebase_database.child("users").child("contributors").child(local_id).child(
                'interested_pitches').get().val()).values())]
    except TypeError as e:
        interested_pitches = []

    P = []
    if(data.each()):
        for user in data.each():
            pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
            for pitch in pitches.each():
                p = pitch.val()
                d = firebase_database.child("users/pitches/" + local_id + "/" + pitch.key() + "/" + "contributors").get().val()
                contributors = '0'
                if (d):
                    contributors = len([x['contributor_id'] for x in dict(d).values()])
                d = firebase_database.child("users/pitches/" + local_id + "/" + pitch.key() + "/" + "investors").get().val()
                investors = '0'
                if (d):
                    investors = len([x['investor_id'] for x in dict(d).values()])
                d = {'pitch_key': pitch.key(), 'title': p.get('title', "No Title Found"),'body': p.get('description', "No Description Found"),
                     'date': p.get('date_created'), 'status': p.get('status', "active"), 'file': p.get("file"), 'gist':p.get('gist'),
                     "contributors": contributors, "investors": investors}

                if(d['pitch_key'] in interested_pitches):
                    d['interested'] = True
                    P.append(d)
    return render(request, 'contributor/current_projects.html', {'pitches': P, 'investor_key':local_id, 'chats':chat_details})


def chat_window(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']
    if ('chatId' in request.POST):
        chatId = request.POST['chatId']
    else:
        chatId = ''
    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("contributors").child(local_id).child("chatrooms_ids").get()
    chat_details = []
    name = ''
    if (chatrooms.each()):
        for chatroom in chatrooms.each():
            print(chatroom.val())
            if ('pitcher_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['pitcher_id'], 'pitchers'))

        for i, (a, b, c) in enumerate(chat_details):
            investor = firebase_database.child("users").child(c).child(b).get()
            if(chat_details[i][0]==chatId):
                name = investor.val().get("firstname", 'noname')
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname'), chat_details[i][2])

    print("CHAT:", chat_details)
    #########################################

    return render(request, "contributor/chat_window.html", {'chatId':chatId, 'chats':chat_details, 'name':name})

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
