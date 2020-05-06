from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

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
    if('uid' in request.session.keys()):
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']

        #########  get chatrooms  ############
        chatrooms = firebase_database.child("users").child("pitchers").child(local_id).child("chatrooms_ids").get()
        chat_details = []
        if(chatrooms.each()):
            for chatroom in chatrooms.each():
                if('investor_id' in chatroom.val()):
                    chat_details.append((chatroom.val()['key'], chatroom.val()['investor_id'], 'investors'))
                else:
                    chat_details.append((chatroom.val()['key'], chatroom.val()['contributor_id'], 'contributors'))

            for i,(a,b,c) in enumerate(chat_details):
                investor = firebase_database.child("users").child(c).child(b).get()
                chat_details[i] = (chat_details[i][0], investor.val()['firstname'], chat_details[i][2])

        print(chat_details)
        #########################################

        data = firebase_database.child("users").child("pitches").child(local_id).child().get().val()
        if(data==None):
            return render(request, 'pitcher/dashboard.html')
        P = []
        pitches = firebase_database.child("users").child("pitches").child(local_id).get()
        for pitch in pitches.each():
            p = pitch.val()
            d = firebase_database.child("users/pitches/"+local_id+"/"+pitch.key()+"/"+"contributors").get().val()
            contributors = '0'
            if(d):
                contributors = len([x['contributor_id'] for x in dict(d).values()])
            d = firebase_database.child("users/pitches/" + local_id + "/" + pitch.key() + "/" + "investors").get().val()
            investors = '0'
            if(d):
                investors = len([x['investor_id'] for x in dict(d).values()])
            d = {'key':pitch.key(), 'title': p.get('title') , 'body': p.get('description'), 'date': p.get('date_created'),
                 'status': p.get('status'), 'file': p.get("url"), "conrtibutors": contributors, "investors": investors}
            d['tags'] = [p.get('filename')]
            d['gist'] = p.get('gist')
            P.append(d)
        return render(request, 'pitcher/dashboard.html', {'pitches':list(P), 'chats':chat_details})
    else:
        return render(request, 'pitcher/dashboard.html')

def new_pitch(request):
    if(len(request.POST)!=0):
        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')
        status = 'active'
        date = str(datetime.datetime.now())
        contributors = []
        investors = []
        userid = request.session['email']
        data = {"title": title, "description": description, "status":status, "date_created":date, "contributors":{}, "investors":{}}

        if(file!=None):
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            #print(uploaded_file_url)
            #entry = AddDetails(title=title, description=description, video=filename, userid=userid)
            data["filename"]=filename
            idtoken = request.session['uid']  # getting id of the current logged in user
            account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
            local_id = account_info['users'][0]['localId']
            outfile = 'media/' + filename
            firebase_storage.child("pitches/" + local_id + "/" + filename).put(outfile)
            firebase_database.child('users').child('pitches').child(local_id).push(data)
        else:
            #entry = AddDetails(title=title, description=description, video=None, userid=userid)
            idtoken = request.session['uid']  # getting id of the current logged in user
            account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
            local_id = account_info['users'][0]['localId']
            firebase_database.child('users').child('pitches').child(local_id).push(data)
        return redirect('/pitcher/dashboard')
    else:
        return render(request, 'pitcher/new pitch.html')

def edit_pitch(request):
    print("POST",request.POST)
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
        data = {"title": title, "description": description, "status": status, "date_created": date, "contributors": {},
                "investors": {}}

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
        else:
            idtoken = request.session['uid']  # getting id of the current logged in user
            account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
            local_id = account_info['users'][0]['localId']
        #data = firebase_database.child("users").child("pitches").child(local_id).get()
        #pitch_id = ""
        #for pitch in data.each():
        #    temp = pitch.val()
        #    if temp['title'] == title:
        #        pitch_id = temp.key()
        #        break

        firebase_database.child("users").child("pitches").child(local_id).child(key).update(data)
        return redirect("/pitcher/dashboard")
    else:
        key = request.POST.get('key')
        idtoken = request.session['uid']  # getting id of the current logged in user
        account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
        local_id = account_info['users'][0]['localId']
        data = firebase_database.child("users").child("pitches").child(local_id).child(key).get().val()
        title = data['title']
        description = data['description']
        status = data['status']
        active = True if status=='active' else False
        return render(request, 'pitcher/edit_pitch.html', {'title':title, 'body':description,'key':key, 'active':active})

def delete_pitch(request):
    key = request.POST.get('key')
    print(key)
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']
    firebase_database.child("users").child("pitches").child(local_id).child(key).remove()
    return redirect("/pitcher/dashboard")

def chat_window(request):
    idtoken = request.session['uid']  # getting id of the current logged in user
    account_info = firebase_auth.get_account_info(idtoken)  # to get account info of the user
    local_id = account_info['users'][0]['localId']
    chatId = request.POST['chatId']
    return render(request, "pitcher/chat_window.html", {'chatId':chatId})


def logout(request):
    try:
        del request.session['uid']
        del request.session['role']
        del request.session['email']
    except:
        print("Some error while logging out!")
    return redirect('/users/home')
