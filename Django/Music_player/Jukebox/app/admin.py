from django.contrib import admin
from .models import *

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')

admin.site.register(Genre, GenreAdmin)
admin.site.register(Song)
admin.site.register(Playlist)
