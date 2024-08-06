from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import *
from .models import *

def Home(request):
    Genres = Genre.objects.all  ()
    return render(request, 'app/genre.html', {'Genres': Genres})

def genre_detail(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)
    songs = Song.objects.filter(genre=genre)
    user_playlist = Playlist.objects.filter(owner=request.user)

    context = {
        'playlists': user_playlist,
        'genre': genre,
        'songs': songs,
    }
    return render(request, 'app/genre_detail.html', context)

@login_required(login_url='Home')
def creating_playlist(request):
    form = PlaylistForm()
    playlists = Playlist.objects.all()

    if request.method == "POST":
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.owner = request.user
            form.save()
            return redirect('playlist_overview')

    context = {'form': form, 'playlist': playlists}
    return render(request, 'app/create_playlist.html', context)

@login_required(login_url='Home')
def playlist_overview(request):
    user_playlist = Playlist.objects.filter(owner=request.user)

    context = {'playlists': user_playlist}
    return render(request, 'app/playlist_overview.html',context )

@login_required(login_url='Home')
def deleting_playlist(request, pk):
    playlist = Playlist.objects.get(id=pk)
    playlist.delete()
    return redirect('playlist_overview')

@login_required(login_url='Home')
def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    songs = playlist.songs.all()
    return render(request, 'app/playlist_detail.html', {'playlist': playlist, 'songs': songs})