from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='contributor-dashboard'),
    path('current_projects/', views.current_projects, name='contributor-current_projects'),
    path('chat_window/', views.chat_window, name='contributor-chat_window'),
    path('delete_contributor/', views.delete_account, name='contributor-delete_contributor'),
    path('logout/', views.logout, name='contributor-logout'),
]