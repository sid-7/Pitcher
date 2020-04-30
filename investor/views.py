from django.shortcuts import render, redirect
from pitcher.models import AddDetails

# Create your views here.
def dashboard(request):
    all_pitches = AddDetails.objects.all()
    # u = AddDetails(userid=userid)
    # all_pitches = u.objects
    p = []
    for pitches in all_pitches:
        p.append({'title': pitches.title, 'body': pitches.description, 'tags': ['tag1', 'tag2']})
    print(p)

    return render(request, 'investor/dashboard.html', {'pitches': p})

def current_projects(request):
    return render(request, 'investor/dashboard.html')

def logout(request):
    try:
        del request.session['role']
        del request.session['email']
    except:
        print("Some error while logging out!")
    return redirect('/user/home')