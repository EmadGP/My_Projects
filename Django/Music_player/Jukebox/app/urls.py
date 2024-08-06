from django.urls import path
from login.views import sign_out
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
    path('playlist/', views.playlist_overview, name='playlist_overview'),
    path('playlist/create/', views.creating_playlist, name='creating_playlist'),
    path('playlist/delete/<int:pk>/', views.deleting_playlist, name='deleting_playlist'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path("sign_out", sign_out, name="sign_out"),
]