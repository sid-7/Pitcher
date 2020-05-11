from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='pitcher-dashboard'),
    path('new_pitch/',views.new_pitch, name='pitcher-new_pitch'),
    path('edit_pitch/',views.edit_pitch, name='pitcher-edit_pitch'),
    path('delete_pitch/',views.delete_pitch, name='pitcher-delete_pitch'),
    path('chat_window/', views.chat_window, name='pitcher-chat_window'),
    path('delete_pitcher/', views.delete_account, name='pitcher-delete_pitcher'),
    path('logout/', views.logout, name = 'pitcher-logout'),

]