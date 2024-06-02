from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Genre, Song

def Home(request):

    Genres = Genre.objects.all()
    return render(request, 'app/genre.html', {'Genres': Genres})

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    songs = Song.objects.filter(genre=genre)
    return render(request, 'app/genre_detail.html', {'genre': genre, 'songs': songs})