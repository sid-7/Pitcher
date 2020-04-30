from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('home/',views.home, name='users-home'),
    path('login/',views.login, name='users-login'),
    path('signup/',views.signup, name='users-signup'),
    path('about/',views.about, name='users-about'),
    path('contact/',views.contact, name='users-contact'),
]