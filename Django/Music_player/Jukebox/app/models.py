from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)  # Add image field


    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return self.title