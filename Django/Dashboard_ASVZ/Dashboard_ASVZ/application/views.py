from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render

@login_required(login_url='index')
def home(request):
    return render(request, "application/home.html")