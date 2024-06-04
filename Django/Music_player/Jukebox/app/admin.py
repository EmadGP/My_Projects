from django.contrib import admin
from .models import Song, Genre

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

admin.site.register(Genre, GenreAdmin)
admin.site.register(Song)
