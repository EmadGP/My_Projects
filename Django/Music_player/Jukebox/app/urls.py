from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),

]