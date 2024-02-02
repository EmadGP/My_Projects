from django import forms
from crispy_forms.helper import FormHelper
from django.urls import reverse_lazy
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class RegistrationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('sign_up')
        # self.helper.form_method = "POST"
        # self.helper.add_input(Submit('submit', 'Submit'))


    ROLE_CHOICES = [
        ('Docent', 'Docent'),
        ('Student', 'Student'),
        # ('Zakelijk', 'Zakelijk'),
    ]
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    role= forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect())


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('sign_in')
        # self.helper.form_method = 'POST'
        # self.helper.add_input(Submit('submit', 'Login'))
