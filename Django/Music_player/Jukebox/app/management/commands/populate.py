import random
from django.core.management.base import BaseCommand
from faker import Faker
from app.models import Genre, Song

class Command(BaseCommand):
    Song.objects.all().delete()
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        genre_names = ["Rock", "Pop", "Jazz", "Electronic", "Hip Hop", ]  # Custom genre list
        genres = [Genre.objects.get_or_create(name=genre_name)[0] for genre_name in genre_names]

        for _ in range(100):  # Adjust the range for the number of records you want
            Song.objects.create(
                title=fake.sentence(nb_words=2),  # Fake song title
                artist=fake.name(),  # Fake artist name
                genre=random.choice(genres),  # Random genre from the custom list
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))
