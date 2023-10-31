from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from .tokens import generate_token


def index(request):
    return render(request, 'login/index.html')

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
            return redirect("home")

        if not isinstance(voornaam,str):
            messages.error(request, "Gebruik alleen letters voor uw naam!")
            return redirect("home")

        if not isinstance(achternaam,str):
            messages.error(request, "Gebruik alleen letters voor uw achternaam!")
            return redirect("home")

        if User.objects.filter(username=user_name):
            messages.error(request, "Gebruikersnaam bestaat al!")
            return redirect("home")

        myuser = User.objects.create_user(user_name, mail, wachtwoord)
        myuser.first_name = voornaam
        myuser.last_name = achternaam
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Uw account is aangemaakt!")

        # <-------------- Welcome Email -------------->

        subject = "Welkom bij Wegwijzer D&S!"
        message = "Beste " + str(
            myuser.first_name) + ", \n \n" + """Welkom bij Wegwijzer D&S!\nWe hebben u zojuist een bevestigingsmail gestuurd. Gelieve uw e-mailadres te bevestigen om uw account te activeren.\n \nAlvast hartelijk dank!\n \nMet vriendelijke groet,\n \n \nHet ondersteuningsteam van Wegwijzer D&S"""
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # <-------------- Confirmation Email -------------->

        current_site = get_current_site(request)
        subject2 = "Bevestig uw account"
        message2 = render_to_string("email_confirmation.html", {
            "name": myuser.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(myuser.pk)),
            "token": generate_token.make_token(myuser)
        })
        email = EmailMessage(
            subject2,
            message2,
            from_email,
            to_list
        )
        email.fail_silently = False
        email.send()

        return redirect('home')

    return render(request, 'login/index.html')

# <-------------- Account Login -------------->

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("user")
        wachtwoord = request.POST.get("wachtwoord")

        user = authenticate(username=username, password=wachtwoord)

        if user is not None:
            login(request, user)
            voornaam = user.first_name
            return render(request, "login/index.html", {"voornaam": voornaam})
        else:
            messages.error(request, "Gegevens komen niet overeen")
            return redirect("home")

    return render(request, 'login/index.html')


# <-------------- Account Logout -------------->

def sign_out(request):
    logout(request)
    messages.success(request, "Uw bent uitgelogd!")
    return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect("home")

    else:
        return render(request, "activation_failed.html")
