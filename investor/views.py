from django.shortcuts import render, redirect

import pyrebase
########################  firebase authentication  ##################################
config = {
 
}
firebase = pyrebase.initialize_app(config)
firebase_auth = firebase.auth()
firebase_database = firebase.database()
##########################################################################################

# Create your views here.
def dashboard(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except Exception as e:
        return logout(request)

    data = firebase_database.child("users").child("pitches").get()
    try:
        interested_pitches = [x['pitch_id'] for x in (dict(firebase_database.child("users").child("investors").child(local_id).child('interested_pitches').get().val()).values())]
    except:
        interested_pitches = []
    print(interested_pitches)

    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("investors").child(local_id).child("chatrooms_ids").get()
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
    if(data.each()):
        for user in data.each():
            pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
            for pitch in pitches.each():
                p = pitch.val()
                d = firebase_database.child(
                    "users/pitches/" + local_id + "/" + pitch.key() + "/" + "contributors").get().val()
                contributors = 0
                if (d):
                    contributors = len([x['contributor_id'] for x in dict(d).values()])
                d = firebase_database.child(
                    "users/pitches/" + local_id + "/" + pitch.key() + "/" + "investors").get().val()
                investors = 0
                if (d):
                    investors = len([x['investor_id'] for x in dict(d).values()])

                d = {'pitch_key': pitch.key(), "pitcher_key":user.key(), 'title': p.get('title'), 'file':p.get('file'),
                     'body': p.get('description'),'date': p.get('date_created'),'status': p.get('status'), 'gist':p.get('gist'),
                     "contributors": contributors, "investors": investors}

                d['interested'] = True if(d['pitch_key'] in interested_pitches) else False
                P.append(d)
    return render(request, 'investor/dashboard.html', {'pitches':list(P), 'investor_key':local_id, 'chats':chat_details})

def current_projects(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except Exception as e:
        return logout(request)

    data = firebase_database.child("users").child("pitches").get()
    try:
        interested_pitches = [x['pitch_id'] for x in (dict(firebase_database.child("users").child("investors").child(local_id).child('interested_pitches').get().val()).values())]
    except TypeError as e:
        interested_pitches = []

    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("investors").child(local_id).child("chatrooms_ids").get()
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
    if(data.each()):
        for user in data.each():
            pitches = firebase_database.child("users").child("pitches").child(user.key()).get()
            for pitch in pitches.each():
                p = pitch.val()
                d = {'pitch_key': pitch.key(), "pitcher_key":user.key(), 'title': p.get('title'), 'body': p.get('description'), 'file':p.get('file'),
                     'date': p.get('date_created'),'status': p.get('status'), 'gist':p.get('gist'),
                     "conrtibutors": p.get('contributors'), "investors": p.get('investors')}
                if(d['pitch_key'] in interested_pitches):
                    d['interested'] = True
                    P.append(d)
    return render(request, 'investor/dashboard.html', {'pitches': P, 'investor_key':local_id, 'chats':chat_details})

def chat_window(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except Exception as e:
        return logout(request)
    if('chatId' in request.POST):
        chatId = request.POST['chatId']
    else:
        chatId=''

    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("investors").child(local_id).child("chatrooms_ids").get()
    chat_details, name = [], 'None'
    if (chatrooms.each()):
        for chatroom in chatrooms.each():
            print(chatroom.val())
            if ('pitcher_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['pitcher_id'], 'pitchers'))

        for i, (a, b, c) in enumerate(chat_details):
            investor = firebase_database.child("users").child(c).child(b).get()
            if(chat_details[i][0]==chatId):
                name = investor.val().get('firstname')
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname'), chat_details[i][2])

    print("CHAT:", chat_details)
    #########################################

    return render(request, "investor/chat_window.html", {'chatId':chatId, 'name':name, 'chats':chat_details})

def delete_account(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except Exception as e:
        return logout(request)

    pitcher_to_pitch_ids = [] # ['pitcher_id','pitch_id']

    chatroom_ids = []
    chatrooms = firebase_database.child("users").child("investors").child(local_id).child("chatrooms_ids").get()
    if chatrooms.each():
        for chatroom in chatrooms.each():
            chatroom_ids.append(chatroom.val()['key'])

    for chatroom in chatroom_ids:
        firebase_database.child("users").child("chatrooms").child(chatroom).remove()


    interested_pitches = firebase_database.child("users").child("investors").child(local_id).child("interested_pitches").get()

    if interested_pitches.each():
        for pitch in interested_pitches.each():
            l=[]
            l.append(pitch.val()['pitcher_id'])
            l.append(pitch.val()['pitch_id'])
            pitcher_to_pitch_ids.append(l)


    for pitcher in pitcher_to_pitch_ids:
        investors = firebase_database.child("users").child("pitches").child(pitcher[0]).child(pitcher[1]).child("investors").get()
        if investors.each():
            for investor in investors.each():
                if investor.val()['investor_id'] == local_id:
                    firebase_database.child("users").child("pitches").child(pitcher[0]).child(pitcher[1]).child("investors").child(investor.key()).remove()


    for entry in pitcher_to_pitch_ids:
        investors_in_pitchers = firebase_database.child("users").child("pitchers").child(entry[0]).child("interested_investors").get()
        if investors_in_pitchers.each():
            for investor in investors_in_pitchers.each():
                if investor.val()['investor_id'] == local_id:
                    firebase_database.child("users").child("pitchers").child(entry[0]).child("interested_investors").child(investor.key()).remove()

    firebase_database.child("users").child("investors").child(local_id).remove()

    return render(request, "users/home.html")

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
        del request.session['uid']
    except:
        print("Some error while logging out!")
    return redirect('/users/home')
