from django.contrib import admin

# Register your models here.

from .models import Klas, Bedrijf

admin.site.register(Klas)
admin.site.register(Bedrijf)
