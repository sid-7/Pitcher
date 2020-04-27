from django.urls import path

from . import views

urlpatterns = [
    path('register',views.register, name='register'),
    path('add_to_database',views.add_to_database, name='add_to_database')
]