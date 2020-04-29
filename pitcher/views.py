from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from pitcher.models import AddDetails


# Create your views here.
def dashboard(request):
    return render(request, 'pitcher/dashboard.html')


def add_details(request):
    return render(request, 'pitcher/add_details.html')


def add_details_to_database(request):
    title = request.POST['title']
    description = request.POST['description']
    video = request.FILES["video"]
    fs = FileSystemStorage()
    filename = fs.save(video.name, video)
    uploaded_file_url = fs.url(filename)
    print(uploaded_file_url)
    entry = AddDetails(title=title, description=description, video=filename)
    entry.save()
    print("entry created")
    return render(request, 'pitcher/dashboard.html')


