from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pitcher.models import AddDetails


# Create your views here.
def dashboard(request):
    # pitches = all pitches    ########
    # {'pitches': pitches}
    if(True):
        userid = 'n'
        all_pitches = AddDetails.objects.filter(userid=userid).all()
        # u = AddDetails(userid=userid)
        # all_pitches = u.objects
        p = []
        for pitches in all_pitches:
            p.append({'title':pitches.title, 'body':pitches.description, 'tags':['tag1', 'tag2']})
        print(p)
        return render(request, 'pitcher/dashboard.html', {'pitches':p})
    else:
        return render(request, 'pitcher/dashboard.html')

def new_pitch(request):
    print(request.POST)
    if(len(request.POST)!=0):
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')
        if(video!=None):
            fs = FileSystemStorage()
            filename = fs.save(video.name, video)
            uploaded_file_url = fs.url(filename)
            print(uploaded_file_url)
            entry = AddDetails(title=title, description=description, video=filename)
        else:
            entry = AddDetails(title=title, description=description, video=None)
        entry.save()
        return render(request, 'pitcher/dashboard.html')
    else:
        return render(request, 'pitcher/new pitch.html')

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
    except:
        print("Some error while logging out!")
    return render(request, 'users/home.html')
