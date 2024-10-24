from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render

def index(request):
    return render(request, 'authentication/index.html')

# <-------------- Account Registration -------------->
def sign_up(request):
    if request.method == "POST":
        voornaam = request.POST.get("voornaam")
        achternaam = request.POST.get("achternaam")
        mail = request.POST.get("mail")
        wachtwoord = request.POST.get("wachtwoord")
        user_name = voornaam +" " + achternaam

        if User.objects.filter(email=mail):
            messages.error(request, "Email is al in gebruik! ")
            return redirect("index")

        if not isinstance(voornaam,str):
            messages.error(request, "Gebruik alleen letters voor uw naam!")
            return redirect("index")

        if not isinstance(achternaam,str):
            messages.error(request, "Gebruik alleen letters voor uw achternaam!")
            return redirect("index")

        if User.objects.filter(username=user_name):
            messages.error(request, "Gebruikersnaam bestaat al!")
            return redirect("index")

        myuser = User.objects.create_user(user_name, mail, wachtwoord)
        myuser.first_name = voornaam
        myuser.last_name = achternaam
        myuser.is_active = True
        myuser.save()

        messages.success(request, "Uw account is aangemaakt!")

    return render(request, 'authentication/index.html')

# <-------------- Account Login -------------->

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("user")
        wachtwoord = request.POST.get("wachtwoord")

        user = authenticate(username=username, password=wachtwoord)

        if user is not None:
            login(request, user)
            voornaam = user.first_name
            return redirect("home")
        else:
            messages.error(request, "Gegevens komen niet overeen")
            return redirect("index")

    return render(request, 'authentication/index.html')


# <-------------- Account Logout -------------->

def sign_out(request):
    logout(request)
    messages.success(request, "Uw bent uitgelogd!")
    return redirect('index')