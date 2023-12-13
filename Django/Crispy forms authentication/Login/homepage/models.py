from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Klas(models.Model):
    naam = models.CharField(max_length=100)
    docent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    studenten = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='klassen', blank=True)
    beschrijving = models.TextField(blank=True)  # Added a description field

    def __str__(self):
        return self.naam