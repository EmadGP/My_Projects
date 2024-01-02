from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Klas(models.Model):
    naam = models.CharField(max_length=100)
    docent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    studenten = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='klassen', blank=True)
    beschrijving = models.TextField(blank=True)


    def __str__(self):
        return self.naam

class StagePeriode(models.Model):
    klas = models.ForeignKey('Klas', on_delete=models.CASCADE)
    start_datum = models.DateField()
    eind_datum = models.DateField()
    min_uren = models.IntegerField()
    verwachte_uren = models.IntegerField()
    stage_soort = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.klas.naam} - {self.stage_soort} ({self.start_datum} to {self.eind_datum})"

