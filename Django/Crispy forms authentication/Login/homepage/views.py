import time as t
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import Klas, StagePeriode, Bedrijf, Job
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

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
        student = None
        if request.method == 'POST':
            form = StudentSearchForm(request.POST)
            if form.is_valid():
                student_username = form.cleaned_data['search_query']
                try:
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

# @login_required(login_url='index')
# def zakelijk_home(request):
#     bedrijven = Bedrijf.objects.filter(zakelijk_gebruiker=request.user)
#     return render(request, 'homepage/zakelijk_home.html', {'bedrijven': bedrijven})

def student_profile(request, student_id):
    student = get_object_or_404(User, id=student_id, groups__name='Studenten_Groep')
    companies = Company.objects.filter(added_by=student)

    if request.method == 'POST':
        if request.user.role == "Docent":
            student.notes = request.POST.get('notes', '')
            student.save()
    return render(request, 'homepage/student_profile.html', {
        'student': student,
        'companies': companies,
                                                             })

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

@login_required(login_url='index')
def bedrijf_details(request, bedrijf_id):
    bedrijf = get_object_or_404(Bedrijf, id=bedrijf_id)
    jobs = bedrijf.jobs.all()

    job_form = CreateJobForm()

    status_forms = {job.id: UpdateJobStatusForm(instance=job) for job in jobs}

    if request.method == 'POST':
        if 'create_job' in request.POST:
            job_form = CreateJobForm(request.POST)
            if job_form.is_valid():
                job = job_form.save(commit=False)
                job.bedrijf = bedrijf
                job.save()
                return redirect('bedrijf_details', bedrijf_id=bedrijf.id)
        else:
            for job in jobs:
                form = UpdateJobStatusForm(request.POST, instance=job, prefix=f'job_{job.id}')
                if form.is_valid():
                    form.save()

    return render(request, 'homepage/bedrijf_details.html', {
        'bedrijf': bedrijf,
        'jobs': jobs,
        'job_form': job_form,
        'status_forms': status_forms
    }
                  )

def add_bedrijf(request, stage_id):
    stage = get_object_or_404(StagePeriode, id=stage_id)

    if request.method == 'POST':
        form = BedrijfForm(request.POST)
        if form.is_valid():
            bedrijf = form.save(commit=True)
            bedrijf.stage_periode = stage
            bedrijf.save()
            return redirect('stage_details', klas_id=stage.klas.id, stage_periode_id=stage.id)
    else:
        form = BedrijfForm()

    return render(request, 'homepage/add_bedrijf.html', {'form': form, 'stage': stage})

@login_required(login_url='index')
def bedrijf_delete(request, bedrijf_id):
    bedrijf = get_object_or_404(Bedrijf, id=bedrijf_id)

    bedrijf.delete()
    return redirect(stage_details, bedrijf.stage_periode.klas.id, bedrijf.stage_periode.id)


@login_required(login_url='index')
def stage_details(request, klas_id, stage_periode_id):
    klas = get_object_or_404(Klas, id=klas_id)
    stage_periode = get_object_or_404(StagePeriode, id=stage_periode_id)
    bedrijven = Bedrijf.objects.filter(stage_periode=stage_periode)

    # Check if the form is submitted
    if request.method == 'POST':
        selected_students = request.POST.getlist('selected_students')
        klas.studenten.add(*selected_students)
        messages.success(request, f'Students added to {stage_periode.stage_soort} stage period.')
        return redirect('stage_details', klas_id=klas.id, stage_periode_id=stage_periode.id)

    return render(request, 'homepage/stage_details.html', {
        'klas': klas,
        'stage_periode': stage_periode,
        'bedrijven': bedrijven,
    })

@login_required(login_url='index')
def delete_student_from_stage(request, klas_id, stage_periode_id, student_id):
    klas = get_object_or_404(Klas, id=klas_id)
    stage_periode = get_object_or_404(StagePeriode, id=stage_periode_id)
    student = get_object_or_404(User, id=student_id, groups__name='Studenten_Groep')

    if request.method == 'POST':
        klas.studenten.remove(student)
        messages.success(request, f'Student {student.username} removed from {stage_periode.stage_soort} stage period.')

    return redirect('stage_details', klas_id=klas.id, stage_periode_id=stage_periode.id)

def add_company(request):
    user = request.user
    if request.method == 'POST':
        if user.role == "Docent":
            form = CompanyFormDocent(request.POST)
            if form.is_valid():
                company = form.save(commit=False)
                company.added_by = request.user
                company.save()
                return redirect('docent_home')

        elif user.role == "Student":
            form = CompanyForm(request.POST)
            if form.is_valid():
                company = form.save(commit=False)
                company.added_by = request.user
                company.save()
                return redirect('student_home')
    else:
        if user.role == "Docent":
            form = CompanyFormDocent()
        elif user.role == "Student":
            form = CompanyForm()

    return render(request, 'homepage/add_company.html', {'form': form})

def delete_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)
    company.delete()
    return redirect('list_companies')


def list_companies(request):
    companies = Company.objects.filter(added_by=request.user)
    return render(request, 'homepage/list_companies.html', {'companies': companies})

def update_company_status(request, company_id):
    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        form = CompanyStatusUpdateForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('list_companies')
        else:
            return render(request, 'homepage/update_company_status.html', {'form': form, 'company': company})

    form = CompanyStatusUpdateForm(instance=company)
    return render(request, 'homepage/update_company_status.html', {'form': form, 'company': company})
def add_company_note(request, company_id):
    company = Company.objects.get(pk=company_id)

    if request.method == 'POST':
        form = CompanyNoteForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            return redirect('student_home')
    else:
        form = CompanyNoteForm(instance=company)

    return render(request, 'homepage/add_company_note.html', {'form': form, 'company': company})

def Aangenomen_company(request, company_id):
    company = get_object_or_404(Company, pk=company_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'Aangenomen':
            company.status = new_status
            company.save()
            messages.success(request, 'Status updated successfully.')
        else:
            messages.error(request, 'Invalid status.')

        t.sleep(2)
        return redirect('list_companies')

    form = CompanyStatusUpdateForm(instance=company)
    return render(request, 'homepage/update_company_status.html', {'form': form, 'company': company})