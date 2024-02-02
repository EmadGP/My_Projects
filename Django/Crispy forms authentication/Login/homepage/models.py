# models.py

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
    stage_periode = models.ForeignKey("StagePeriode", null=True, on_delete=models.CASCADE, related_name='bedrijven')
    zakelijk_gebruiker = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='bedrijven')

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

    def delete(self, *args, **kwargs):
        self.klas.studenten.clear()
        super().delete(*args, **kwargs)

class Job(models.Model):
    STATUS_CHOICES = [
        ('Beschikbaar', 'Beschikbaar'),
        ('Vol', 'Vol'),
    ]

    bedrijf = models.ForeignKey("Bedrijf", on_delete=models.CASCADE, related_name='jobs')
    omschrijving = models.TextField()
    start_datum = models.DateField()
    eind_datum = models.DateField()
    gevraagde_vaardigheden = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Beschikbaar')

    def __str__(self):
        return f"{self.bedrijf.name} - {self.omschrijving}"


class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField()
    status_choices = [
        ('Afgewezen', 'Afgewezen'),
        ('Wachtend', 'Wachtend'),
        ('Aangenomen', 'Aangenomen'),
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance is being updated
            original = Company.objects.get(pk=self.pk)
            if original.status != 'Aangenomen' and self.status == 'Aangenomen':
                self._status_changed = True
            else:
                self._status_changed = False
        else:
            self._status_changed = False

        super().save(*args, **kwargs)
