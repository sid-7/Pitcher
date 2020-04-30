from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pitcher.models import AddDetails


# Create your views here.
def dashboard(request):
    # pitches = all pitches    ########
    # {'pitches': pitches}
    if(True):
        userid = request.session['email'] #'nisarmonil@gmail.com'
        all_pitches = AddDetails.objects.filter(userid=userid).all()
        # u = AddDetails(userid=userid)
        # all_pitches = u.objects
        p = []
        for pitches in all_pitches:
            p.append({'title':pitches.title, 'body':pitches.description, 'tags':['tag1', 'tag2']})

        return render(request, 'pitcher/dashboard.html', {'pitches':p})
    else:
        return render(request, 'pitcher/dashboard.html')

def new_pitch(request):
    if(len(request.POST)!=0):
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')
        userid = request.session['email']

        if(video!=None):
            fs = FileSystemStorage()
            filename = fs.save(video.name, video)
            uploaded_file_url = fs.url(filename)
            #print(uploaded_file_url)
            entry = AddDetails(title=title, description=description, video=filename, userid=userid)
        else:
            entry = AddDetails(title=title, description=description, video=None, userid=userid)
        entry.save()
        return redirect('/pitcher/dashboard')
    else:
        return render(request, 'pitcher/new pitch.html')

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
    except:
        print("Some error while logging out!")
    return redirect('/user/home')
