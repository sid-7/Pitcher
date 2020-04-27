from django.db import models
from django.utils import timezone

class UserRegistration(models.Model):
    email = models.CharField(max_length=30)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    password = models.CharField(max_length=15)
    role = models.CharField(max_length=15)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.first_name

