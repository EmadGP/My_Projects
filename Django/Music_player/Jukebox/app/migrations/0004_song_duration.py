# Generated by Django 5.0.4 on 2024-06-23 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_genre_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.IntegerField(default=0),
        ),
    ]
