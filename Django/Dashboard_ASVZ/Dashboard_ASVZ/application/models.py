from django.db import models
class Pump(models.Model):
    name = models.CharField(max_length=100)
    last_snoozed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name
