from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import request
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .forms import RegistrationForm, LoginForm
from .tokens import generate_token
from .models import MyUser as User


# <-------------- Home Page -------------->

def index(request):

    context = {
        "signup_form": RegistrationForm(),
        "login_form": LoginForm()
    }
    return render(request, 'login/index.html', context)


# <-------------- User Registration -------------->

def sign_up(request):
    form = RegistrationForm(request.POST)
    if form.is_valid():

        if User.objects.filter(email=form.cleaned_data['email']).exists():
            messages.error(request, "Email is already in use!")
            return redirect("index")

        # Check if username is already in use
        username = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already in use!")
            return redirect("index")

        # Additional checks on first_name and last_name
        if not isinstance(form.cleaned_data['first_name'], str):
            messages.error(request, "Use only letters for your first name!")
            return redirect("index")

        if not isinstance(form.cleaned_data['last_name'], str):
            messages.error(request, "Use only letters for your last name!")
            return redirect("index")

        user = User.objects.create(
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            username=form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name'],
            email=form.cleaned_data['email'],
            role=form.cleaned_data['role'],
            is_active=True
        )
        messages.success(request,"Uw account is aangemaakt!")
        user.set_password(form.cleaned_data['password'])
        user.save()

        # <-------------- Group selection -------------->

        role = form.cleaned_data['role']

        if role == 'Docent':
            group_name = 'Docenten_Groep'
        elif role == 'Student':
            group_name = 'Studenten_Groep'
        elif role == 'Zakelijk':
            group_name = 'Zakelijke_Groep'
        else:
            group_name = None
            messages.error(request, "Er is iets misgegaan!")
            redirect("index")

        if group_name:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

        # <-------------- Welcome Email -------------->

        subject = "Welkom bij Wegwijzer D&S!"
        message = "Beste " + str(
            user.first_name) + ", \n \n" + """Welkom bij Wegwijzer D&S!\nWe hebben u zojuist een bevestigingsmail gestuurd. Gelieve uw e-mailadres te bevestigen om uw account te activeren.\n \nAlvast hartelijk dank!\n \nMet vriendelijke groet,\n \n \nHet ondersteuningsteam van Wegwijzer D&S"""
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)

        # <-------------- Confirmation Email -------------->

        current_site = get_current_site(request)
        subject2 = "Bevestig uw account"
        message2 = render_to_string("email_confirmation.html", {
            "name": user.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": generate_token.make_token(user)
        })
        email = EmailMessage(
            subject2,
            message2,
            from_email,
            to_list
        )
        email.fail_silently = False
        email.send()

        return redirect('index')

    context = {
        "signup_form": RegistrationForm(),
        "login_form": LoginForm()
    }

    return render(request, 'login/index.html',context)

# <-------------- User Authentication -------------->

def sign_in(request):
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data['username']
        password = login_form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Docenten_Groep').exists():
                # return render(request, "homepage/docent_home.html")
                return redirect('docent_home')
            elif user.groups.filter(name='Studenten_Groep').exists():
                # return render(request, "homepage/student_home.html")
                return redirect('student_home')
            elif user.groups.filter(name='Zakelijke_Groep').exists():
                # return render(request, "homepage/zakelijk_home.html")
                return redirect('zakelijk_home')

            else:
                return render(request, "login/index.html")
            # login(request, user)
            # voornaam = user.first_name
            # return render(request, "login/index.html", {"voornaam": voornaam})
        else:
            messages.error(request, "Gegevens komen niet overeen")
            return redirect("index")

    context = {
        "signup_form": RegistrationForm(),
        "login_form": LoginForm()
    }

    return render(request, 'login/index.html', context)

# <-------------- Logout -------------->

def sign_out(request):
    logout(request)
    messages.success(request, "Uw bent uitgelogd!")
    return redirect('index')

# <-------------- Account Activation -------------->

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
        return redirect("index")

    else:
        return render(request, "activation_failed.html")