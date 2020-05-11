from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='investor-dashboard'),
    path('current_projects/', views.current_projects, name='investor-current_projects'),
    path('chat_window/', views.chat_window, name='investor-chat_window'),
    path('delete_investor/', views.delete_account, name='investor-delete_investor'),
    path('logout/', views.logout, name='investor-logout'),

]