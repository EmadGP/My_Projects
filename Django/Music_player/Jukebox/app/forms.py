from django import forms
from django.forms import ModelForm

from .models import *

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = "__all__"