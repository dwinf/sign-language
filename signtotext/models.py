from django.db import models

# Create your models here.

class Record(models.Model):
    word = models.CharField(max_length=100)
    audio = models.FileField(blank=True, upload_to="audio/word")