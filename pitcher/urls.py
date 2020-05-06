from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='pitcher-dashboard'),
    path('new_pitch/',views.new_pitch, name='pitcher-new_pitch'),
    path('edit_pitch/',views.edit_pitch, name='pitcher_app-edit_pitch'),
    path('delete_pitch/',views.delete_pitch, name='pitcher_app-delete_pitch'),
    path('logout/', views.logout, name = 'pitcher-logout'),
    path('chat_window/', views.chat_window, name='pitcher_app-chat_window'),
]