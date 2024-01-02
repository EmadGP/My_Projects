from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django import forms


class MyUser(AbstractUser):
    ROLE_CHOICES = [
        ('Docent', 'Docent'),
        ('Student', 'Student'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)



