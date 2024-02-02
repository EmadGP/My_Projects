from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('create_klas/', create_klas, name='create_klas'),
    path('klas_gegevens/<int:klas_id>/', klas_gegevens, name='klas_gegevens'),

    path('add_student/<int:klas_id>/', add_student, name='add_student'),
    path('delete_student/<int:klas_id>/<int:student_id>/', delete_student, name='delete_student'),

    path('homepage/create_stage_periode/<int:klas_id>/', views.create_stage_periode, name='create_stage_periode'),
    path('stage_details/<int:klas_id>/<int:stage_periode_id>/', stage_details, name='stage_details'),

    path('docent_home/', docent_home, name='docent_home'),
    path('student_home/', student_home, name='student_home'),
    # path('zakelijk_home/', zakelijk_home, name='zakelijk_home'),

    path('student_profile/<int:student_id>/', views.student_profile, name='student_profile'),
    path('delete_stage_periode/<int:klas_id>/<int:stage_periode_id>/', views.delete_stage_periode,name='delete_stage_periode'),
    path('delete_student_from_stage/<int:klas_id>/<int:stage_periode_id>/<int:student_id>/', views.delete_student_from_stage, name='delete_student_from_stage'),


    path('bedrijf_details/<int:bedrijf_id>/', bedrijf_details, name='bedrijf_details'),
    path('add_bedrijf/<int:stage_id>/', add_bedrijf, name='add_bedrijf'),
    path('bedrijf_delete/<int:bedrijf_id>/', bedrijf_delete, name='bedrijf_delete'),

    path('add_company/', add_company, name='add_company'),
    path('list_companies/', list_companies, name='list_companies'),
    path('update_company_status/<int:company_id>/', update_company_status, name='update_company_status'),
    path('add_company_note/<int:company_id>/', add_company_note, name='add_company_note'),
    path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('Aangenomen_company/<int:company_id>/', Aangenomen_company, name='Aangenomen_company'),

    # path('link_zakelijk_gebruiker/<int:bedrijf_id>/', link_zakelijk_gebruiker, name='link_zakelijk_gebruiker'),
    #
    # path('create_job/<int:bedrijf_id>/', create_job, name='create_job'),
    # path('delete_job/<int:job_id>/', delete_job, name='delete_job'),
    # path('update_job_status/<int:job_id>/', update_job_status, name='update_job_status'),

]



