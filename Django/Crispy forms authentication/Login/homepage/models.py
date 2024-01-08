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

class Bedrijf(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField()
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()
    stage_periode = models.ForeignKey("StagePeriode", null=True ,on_delete=models.CASCADE, related_name='bedrijven')



    def __str__(self):
        return self.name

class StagePeriode(models.Model):
    klas = models.ForeignKey('Klas', on_delete=models.CASCADE)
    bedrijf = models.ForeignKey(Bedrijf, on_delete=models.CASCADE, null=True, blank=True)
    start_datum = models.DateField()
    eind_datum = models.DateField()
    min_uren = models.IntegerField()
    verwachte_uren = models.IntegerField()
    stage_soort = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.klas.naam} - {self.stage_soort} ({self.start_datum} to {self.eind_datum})"