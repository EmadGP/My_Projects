# urls.py
from django.urls import path
from .views import create_klas, add_student, docent_home, student_home, klas_gegevens, delete_student

urlpatterns = [
    path('create_klas/', create_klas, name='create_klas'),
    path('add_student/<int:klas_id>/', add_student, name='add_student'),
    # path('klassen_list/', klassen_list, name='klassen_list'),
    path('klas_gegevens/<int:klas_id>/', klas_gegevens, name='klas_gegevens'),
    path('delete_student/<int:klas_id>/<int:student_id>/', delete_student, name='delete_student'),
    path('docent_home/', docent_home, name='docent_home'),
    path('student_home/', student_home, name='student_home'),
]
