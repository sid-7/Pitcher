from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='investor-dashboard'),
    path('current_projects/', views.current_projects, name='investor-current_projects'),
    path('logout/', views.logout, name='investor-logout'),
]