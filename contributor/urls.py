from django.contrib import admin
from django.urls import path,include
from contributer import views

urlpatterns = [
    path('dashboard', views.dashboard, 'contributor-dashboard'),
]