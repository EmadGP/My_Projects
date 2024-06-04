from django.urls import path
from login.views import sign_out
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path("sign_out", sign_out, name="sign_out"),

]