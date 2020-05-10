from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .functs import summarizer, extract_tags
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
firebase_storage = firebase.storage()
firebase_auth = firebase.auth()
firebase_database = firebase.database()
##########################################################################################

# Create your views here.
def dashboard(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except:
        return logout(request)

    name = firebase_database.child("users/pitchers").child(local_id).child().get().val()
    name = name.get('firstname')
    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("pitchers").child(local_id).child("chatrooms_ids").get()
    chat_details = []
    if(chatrooms.each()):
        for chatroom in chatrooms.each():
            if('investor_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['investor_id'], 'investors'))
            elif('contributor_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['contributor_id'], 'contributors'))

        for i,(a,b,c) in enumerate(chat_details):
            print("users/{}/{}".format(c,b))
            investor = firebase_database.child("users").child(c).child(b).get()
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname', "NoName"), chat_details[i][2])
    print("chats for pitcher {}: {}".format(local_id[:5], chat_details))
    #########################################
    data = firebase_database.child("users").child("pitches").child(local_id).child().get().val()
    if(data==None):
        return render(request, 'pitcher/dashboard.html', {'chats':chat_details})
    P = []
    pitches = firebase_database.child("users").child("pitches").child(local_id).get()
    for pitch in pitches.each():
        p = pitch.val()
        print(p)
        d = firebase_database.child("users/pitches/"+local_id+"/"+pitch.key()+"/"+"contributors").get().val()
        contributors = 0
        if(d):
            contributors = len([x['contributor_id'] for x in dict(d).values()])
        d = firebase_database.child("users/pitches/" + local_id + "/" + pitch.key() + "/" + "investors").get().val()
        investors = 0
        if(d):
            investors = len([x['investor_id'] for x in dict(d).values()])
        d = {'pitch_key':pitch.key(), 'title': p.get('title', "No Title Found") , 'body': p.get('description', "No Description Found"),
             'date': p.get('date_created'),'status': p.get('status', "active"), 'file': p.get("file"), 'gist':p.get('gist'),
             "contributors": contributors, "investors": investors}
        P.append(d)
    print("Pitches for {}: {}".format(local_id, P))
    return render(request, 'pitcher/dashboard.html', {'pitches':list(P), 'chats':chat_details, 'name':name})

def new_pitch(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except:
        return logout(request)

    if(len(request.POST)!=0):
        title = request.POST.get('title')
        description = request.POST.get('description')
        url = request.POST.get('url')
        status = 'active'
        date = str(datetime.datetime.now())

        data = {"title": title, "description": description, "gist":summarizer(description), "file":url,
                "status":status, "date_created":date, "contributors":{}, "investors":{}}

        print("POST:", request.POST)

        print("DATA:", data)
        firebase_database.child('users').child('pitches').child(local_id).push(data)
        return redirect('/pitcher/dashboard')
    else:
        #########  get chatrooms  ############
        chatrooms = firebase_database.child("users").child("pitchers").child(local_id).child("chatrooms_ids").get()
        chat_details = []
        if (chatrooms.each()):
            for chatroom in chatrooms.each():
                if ('investor_id' in chatroom.val()):
                    chat_details.append((chatroom.val()['key'], chatroom.val()['investor_id'], 'investors'))
                elif ('contributor_id' in chatroom.val()):
                    chat_details.append((chatroom.val()['key'], chatroom.val()['contributor_id'], 'contributors'))

            for i, (a, b, c) in enumerate(chat_details):
                print("users/{}/{}".format(c, b))
                investor = firebase_database.child("users").child(c).child(b).get()
                chat_details[i] = (chat_details[i][0], investor.val()['firstname'], chat_details[i][2])
        print("chats for pitcher {}: {}".format(local_id[:5], chat_details))
        #########################################
        return render(request, 'pitcher/new pitch.html', {'chats':chat_details})

def edit_pitch(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except:
        return logout(request)

    if(len(request.POST) >2):
        key = request.POST.get('key')
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        status = request.POST.get('status')#'active'
        date = str(datetime.datetime.now())
        contributors = []
        investors = []
        userid = request.session['email']
        data = {"title": title, "description": description, "gist":summarizer(description), "status": status,
                "date_created": date, "contributors": {}, "investors": {}}
        if (file != None):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            data["filename"] = filename
            idtoken = request.session['uid']  # getting id of the current logged in user
            account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
            local_id = account_info['users'][0]['localId']
            outfile = 'media/' + filename
            firebase_storage.child("pitches/" + local_id + "/" + filename).put(outfile)

        firebase_database.child("users").child("pitches").child(local_id).child(key).update(data)
        return redirect("/pitcher/dashboard")
    else:
        key = request.POST.get('key')
        data = firebase_database.child("users").child("pitches").child(local_id).child(key).get().val()
        title = data['title']
        description = data['description']
        status = data['status']
        active = True if status=='active' else False

        #########  get chatrooms  ############
        chatrooms = firebase_database.child("users").child("pitchers").child(local_id).child("chatrooms_ids").get()
        chat_details = []
        if (chatrooms.each()):
            for chatroom in chatrooms.each():
                if ('investor_id' in chatroom.val()):
                    chat_details.append((chatroom.val()['key'], chatroom.val()['investor_id'], 'investors'))
                elif ('contributor_id' in chatroom.val()):
                    chat_details.append((chatroom.val()['key'], chatroom.val()['contributor_id'], 'contributors'))

            for i, (a, b, c) in enumerate(chat_details):
                print("users/{}/{}".format(c, b))
                investor = firebase_database.child("users").child(c).child(b).get()
                chat_details[i] = (chat_details[i][0], investor.val()['firstname'], chat_details[i][2])
        print("chats for pitcher {}: {}".format(local_id[:5], chat_details))
        #########################################

        return render(request, 'pitcher/edit_pitch.html', {'title':title, 'body':description,'key':key, 'active':active, 'chats':chat_details})

def delete_pitch(request):
    try:
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
    except:
        return logout(request)

    pitch_id = request.POST.get('key')

    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']

    chatrooms = firebase_database.child("users").child("chatrooms").get()
    chatrooms_ids = []
    if chatrooms.each():
        for chatroom in chatrooms.each():
            if ('pitch_id' in chatroom.val().keys()):
                if chatroom.val()['pitch_id'] == pitch_id:
                    #chatrooms_ids.append(firebase_database.child("users").child("chatrooms").child(chatroom.key())[])
                    firebase_database.child("users").child("chatrooms").child(chatroom.key()).remove()

    investors = firebase_database.child("users").child("pitches").child(local_id).child(pitch_id).child("investors").get()
    investors_ids = []

    if investors.each():
        for investor in investors.each():
            investors_ids.append(investor.val()['investor_id'])

    for investor in investors_ids:
        interested_pitches = firebase_database.child("users").child("investors").child(investor).child("interested_pitches").get()
        if interested_pitches.each():
            for pitch in interested_pitches.each():
                if pitch.val()['pitch_id'] == pitch_id:
                    firebase_database.child("users").child("investors").child(investor).child("interested_pitches").child(pitch.key()).remove()

    contributors = firebase_database.child("users").child("pitches").child(local_id).child(pitch_id).child("contributors").get()
    contributors_ids = []

    if contributors.each():
        for contributor in contributors.each():
            contributors_ids.append(contributor.val()['contributor_id'])

    for contributor in contributors_ids:
        interested_pitches = firebase_database.child("users").child("contributors").child(contributor).child("interested_pitches").get()
        if interested_pitches.each():
            for pitch in interested_pitches.each():
                if pitch.val()['pitch_id'] == pitch_id:
                    firebase_database.child("users").child("contributors").child(contributor).child("interested_pitches").child(pitch.key()).remove()



    firebase_database.child("users").child("pitches").child(local_id).child(pitch_id).remove()

    return redirect("/pitcher/dashboard")

def chat_window(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']
    if ('chatId' in request.POST):
        chatId = request.POST['chatId']
    else:
        chatId = ''
    #########  get chatrooms  ############
    chatrooms = firebase_database.child("users").child("pitchers").child(local_id).child("chatrooms_ids").get()
    chat_details = []
    name = ''
    if (chatrooms.each()):
        for chatroom in chatrooms.each():
            if ('investor_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['investor_id'], 'investors'))
            elif ('contributor_id' in chatroom.val()):
                chat_details.append((chatroom.val()['key'], chatroom.val()['contributor_id'], 'contributors'))

        for i, (a, b, c) in enumerate(chat_details):
            print("users/{}/{}".format(c, b))
            investor = firebase_database.child("users").child(c).child(b).get()
            if(chat_details[i][0]==chatId):
                name = investor.val().get('firstname', "noname")
            chat_details[i] = (chat_details[i][0], investor.val().get('firstname'), chat_details[i][2])

    print("chats for {}: {}".format(local_id, chat_details))
    #########################################

    return render(request, "pitcher/chat_window.html", {'chatId':chatId, 'chats':chat_details, 'name':name})

def logout(request):
    try:
        del request.session['uid']
        del request.session['role']
        del request.session['email']
    except:
        print("Some error while logging out!")
    return redirect('/users/home')

def delete_account(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']

    investor_ids = []

    chatroom_ids = []
    chatrooms = firebase_database.child("users").child("pitchers").child(local_id).child("chatrooms_ids").get()

    if chatrooms.each():
        for chatroom in chatrooms.each():
            #investor_ids.append(chatroom.val()['investor_id'])
            chatroom_ids.append(chatroom.val()['key'])

    # removing chatrooms
    for chatroom in chatroom_ids:
        firebase_database.child("users").child("chatrooms").child(chatroom).remove()

    investor_to_pitches = []
    contributor_to_pitches = []
    pitches = firebase_database.child("users").child("pitches").child(local_id).get()

    if pitches.each():
        for pitch in pitches.each():
            interested_investors = firebase_database.child("users").child("pitches").child(local_id).child(pitch.key()).child("investors").get()
            interested_contributors = firebase_database.child("users").child("pitches").child(local_id).child(pitch.key()).child("contributors").get()

            if interested_investors.each():
                for investor in interested_investors.each():
                    l = []
                    l.append(investor.val()['investor_id'])
                    l.append(pitch.key())
                    investor_to_pitches.append(l)

            if interested_contributors.each():
                for investor in interested_contributors.each():
                    z = []
                    z.append(investor.val()['contributor_id'])
                    z.append(pitch.key())
                    contributor_to_pitches.append(z)

    for user in investor_to_pitches:
        interested_pitches = firebase_database.child("users").child("investors").child(user[0]).child("interested_pitches").get()
        if interested_pitches.each():
            for pitch in interested_pitches.each():
                if pitch.val()['pitch_id'] == user[1]:
                    firebase_database.child("users").child("investors").child(user[0]).child("interested_pitches").child(pitch.key()).remove()

    for user in contributor_to_pitches:
        interested_pitches = firebase_database.child("users").child("contributors").child(user[0]).child("interested_pitches").get()
        if interested_pitches.each():
            for pitch in interested_pitches.each():
                if pitch.val()['pitch_id'] == user[1]:
                    firebase_database.child("users").child("contributors").child(user[0]).child("interested_pitches").child(pitch.key()).remove()

    firebase_database.child("users").child("pitches").child(local_id).remove()
    firebase_database.child("users").child("pitchers").child(local_id).remove()
    return render(request, "users/home.html")