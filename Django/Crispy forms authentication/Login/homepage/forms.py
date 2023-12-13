from django import forms
from .models import Klas

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Klas
        fields = ['naam', 'beschrijving']  # Include the description field in the form

class ClassroomDescriptionForm(forms.ModelForm):
    class Meta:
        model = Klas
        fields = ['beschrijving']

class StudentSearchForm(forms.Form):
    search_query = forms.CharField(label='Zoek student op gebruikersnaam', max_length=100)
