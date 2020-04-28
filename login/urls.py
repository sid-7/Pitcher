from django.urls import path

from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('verify' ,views.verify, name='verify'),
    path('pitcher',views.pitcher,name='pitcher'),
    path('contributor',views.contributor,name='contributor'),
    path('investor',views.investor,name='investor'),
    path('login_page_with_firebase', views.login_page_with_firebase, name='login_page_with_firebase'),
    path('firebase_login', views.firebase_login, name='firebase_login')
]