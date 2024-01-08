from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('create_klas/', create_klas, name='create_klas'),
    path('add_student/<int:klas_id>/', add_student, name='add_student'),
    path('homepage/create_stage_periode/<int:klas_id>/', views.create_stage_periode, name='create_stage_periode'),
    path('klas_gegevens/<int:klas_id>/', klas_gegevens, name='klas_gegevens'),
    path('delete_student/<int:klas_id>/<int:student_id>/', delete_student, name='delete_student'),
    path('docent_home/', docent_home, name='docent_home'),
    path('student_home/', student_home, name='student_home'),
    path('student_profile/<int:student_id>/', views.student_profile, name='student_profile'),
    path('delete_stage_periode/<int:klas_id>/<int:stage_periode_id>/', views.delete_stage_periode,
         name='delete_stage_periode'),
    path('bedrijf_details/<int:bedrijf_id>/', bedrijf_details, name='bedrijf_details'),
    path('add_bedrijf/<int:stage_id>/', add_bedrijf, name='add_bedrijf'),
    path('stage_details/<int:klas_id>/<int:stage_periode_id>/', stage_details, name='stage_details'),
    path('bedrijf_delete/<int:bedrijf_id>/', bedrijf_delete, name='bedrijf_delete'),

]
