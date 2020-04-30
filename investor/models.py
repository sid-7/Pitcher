from django.db import models
from django.utils import timezone

# Create your models here.
class AddDetails(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    video = models.FileField(upload_to='media/pitcher_app/videos/',null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    userid = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=15, default="active")

    def __str__(self):
        return self.title


