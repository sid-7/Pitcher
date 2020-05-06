from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='contributor-dashboard'),
    path('current_projects/', views.current_projects, name='contributor-current_projects'),
    path('to_chatroom/', views.to_chatroom, name='contributor-to_chatroom'),
    path('logout/', views.logout, name='contributor-logout'),
]