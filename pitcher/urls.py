from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='pitcher-dashboard'),
    path('add_details/',views.add_details, name='pitcher-add_details'),
    path('add_details_to_database/',views.add_details_to_database, name='pitcher-add_details_to_database')

]