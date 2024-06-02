from django.core.management.base import BaseCommand
from app.models import Genre, Song


class Command(BaseCommand):
    help = 'Seed initial data for genres and songs'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Genre.objects.all().delete()

        # Seed genres
        genres = ['Rock', 'Pop', 'Hip Hop', 'Jazz', 'Electronic']
        for genre_name in genres:
            genre = Genre.objects.create(name=genre_name)
            self.stdout.write(self.style.SUCCESS(f'Genre "{genre_name}" created'))

        # Seed songs
        songs_data = [
            ('Starboy', 'The Weeknd', 'Pop'),
            ('Song 2', 'Artist 2', 'Pop'),
            ('Song 3', 'Artist 3', 'Hip Hop'),
            ('Song 4', 'Artist 4', 'Jazz'),
            ('Song 5', 'Artist 5', 'Electronic'),
            ('Song 6', 'Artist 5324234', 'Electronic')

        ]
        for title, artist, genre_name in songs_data:
            genre = Genre.objects.get(name=genre_name)
            song = Song.objects.create(title=title, artist=artist, genre=genre)
            self.stdout.write(self.style.SUCCESS(f'Song "{title}" created under genre "{genre_name}"'))
