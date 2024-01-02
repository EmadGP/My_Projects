from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .forms import StudentSearchForm, ClassroomForm, ClassroomDescriptionForm, StagePeriodeForm
from .models import Klas, StagePeriode
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()
# User = settings.AUTH_USER_MODEL
@login_required(login_url='index')
def create_klas(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            klas = form.save(commit=False)
            klas.docent = request.user
            klas.save()
            return redirect('docent_home')
    else:
        form = ClassroomForm()

    return render(request, 'homepage/create_klas.html', {'form': form})
@login_required(login_url='index')
def add_student(request, klas_id):
    klas = get_object_or_404(Klas, id=klas_id)
    if request.user == klas.docent:
        student = None  # Initialize student as None
        if request.method == 'POST':
            form = StudentSearchForm(request.POST)
            if form.is_valid():
                student_username = form.cleaned_data['search_query']
                try:
                    # Query the database for the user with the given username
                    student = User.objects.get(username=student_username)
                    if student.groups.filter(name='Studenten_Groep').exists():
                        klas.studenten.add(student)
                        messages.success(request, f'Student {student_username} toegevoegd aan klas {klas.naam}')
                        return redirect('docent_home')
                    else:
                        messages.error(request, 'Deze gebruiker is geen student in de groep "Studenten_groep".')
                except User.DoesNotExist:
                    messages.error(request, 'Gebruiker niet gevonden.')

        else:
            form = StudentSearchForm()

        return render(request, 'homepage/add_student.html', {'klas': klas, 'form': form, 'student': student})

    messages.error(request, 'Je hebt geen toestemming om studenten toe te voegen aan deze klas.')
    return redirect('index')

@login_required(login_url='index')
def delete_student(request, klas_id, student_id):
    klas = get_object_or_404(Klas, id=klas_id)
    if request.user == klas.docent:
        student = get_object_or_404(klas.studenten, id=student_id)
        klas.studenten.remove(student)
        messages.success(request, f'Student {student.username} verwijderd uit klas {klas.naam}')
    else:
        messages.error(request, 'Je hebt geen toestemming om studenten te verwijderen uit deze klas.')
    return redirect('docent_home')

@login_required(login_url='index')
def docent_home(request):
    docent_klassen = Klas.objects.filter(docent=request.user)
    return render(request, 'homepage/docent_home.html', {'docent_klassen': docent_klassen})


@login_required(login_url='index')
def student_home(request):
    student_klassen = request.user.klassen.all()
    return render(request, 'homepage/student_home.html', {'student_klassen': student_klassen})

def student_profile(request, student_id):
    student = get_object_or_404(User, id=student_id, groups__name='Studenten_Groep')

    if request.method == 'POST':
        if request.user.role == "Docent":
            # Only allow the teacher to edit notes
            student.notes = request.POST.get('notes', '')
            student.save()
    return render(request, 'homepage/student_profile.html', {'student': student})

@login_required(login_url='index')
def klas_gegevens(request, klas_id):
    klas = get_object_or_404(Klas, id=klas_id)
    stage_periodes = StagePeriode.objects.filter(klas=klas)

    if request.user == klas.docent:
        if request.method == 'POST':
            description_form = ClassroomDescriptionForm(request.POST, instance=klas)
            if description_form.is_valid():
                description_form.save()
        else:
            description_form = ClassroomDescriptionForm(instance=klas)
    else:
        description_form = None

    return render(request, 'homepage/klas_gegevens.html', {'klas': klas, 'description_form': description_form, 'stage_periodes': stage_periodes})

@login_required(login_url='index')
def create_stage_periode(request, klas_id):
    klas = get_object_or_404(Klas, id=klas_id, docent=request.user)

    if request.method == 'POST':
        form = StagePeriodeForm(request.POST)
        if form.is_valid():
            stage_periode = form.save(commit=False)
            stage_periode.klas = klas
            stage_periode.save()
            return redirect('klas_gegevens', klas_id=klas.id)
    else:
        form = StagePeriodeForm()

    return render(request, 'homepage/stage_periode_aanmaken.html', {'form': form, 'klas': klas})


@login_required(login_url='index')
def delete_stage_periode(request, klas_id, stage_periode_id):
    klas = get_object_or_404(Klas, id=klas_id, docent=request.user)
    stage_periode = get_object_or_404(StagePeriode, id=stage_periode_id, klas=klas)

    if request.method == 'POST':
        stage_periode.delete()
        return redirect('klas_gegevens', klas_id=klas_id)

    return render(request, 'homepage/delete_stage_periode.html', {'klas': klas, 'stage_periode': stage_periode})