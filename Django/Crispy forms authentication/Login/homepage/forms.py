from django import forms
from .models import *


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

class BedrijfForm(forms.ModelForm):
    class Meta:
        model = Bedrijf
        fields = ['name', 'website', 'phone_number', 'email', 'description']


class LinkZakelijkGebruikerForm(forms.ModelForm):
    class Meta:
        model = Bedrijf
        fields = ['zakelijk_gebruiker']

class CreateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['omschrijving','start_datum', 'eind_datum', 'gevraagde_vaardigheden', 'status']
        widgets = {
            'start_datum': forms.DateInput(attrs={'type': 'date'}),
            'eind_datum': forms.DateInput(attrs={'type': 'date'}),
        }

class UpdateJobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['status']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['added_by']
        fields = ['name', 'email', 'website', 'status']

class CompanyFormDocent(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['added_by']
        fields = ['name', 'email', 'website']


class CompanyStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['status']


class CompanyNoteForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['notes']