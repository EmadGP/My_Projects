from django import forms
from .models import Klas, StagePeriode


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Klas
        fields = ['naam', 'beschrijving']

class ClassroomDescriptionForm(forms.ModelForm):
    class Meta:
        model = Klas
        fields = ['beschrijving']

class StudentSearchForm(forms.Form):
    search_query = forms.CharField(label='Zoek student op gebruikersnaam', max_length=100)

class StagePeriodeForm(forms.ModelForm):
    class Meta:
        model = StagePeriode
        fields = ['start_datum', 'eind_datum', 'min_uren', 'verwachte_uren', 'stage_soort']
        widgets = {
            'start_datum': forms.DateInput(attrs={'type': 'date'}),
            'eind_datum': forms.DateInput(attrs={'type': 'date'}),
        }

