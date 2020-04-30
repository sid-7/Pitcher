from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='pitcher-dashboard'),
    path('new pitch/',views.new_pitch, name='pitcher-new_pitch'),
    path('logout/', views.logout, name = 'pitcher-logout'),
]