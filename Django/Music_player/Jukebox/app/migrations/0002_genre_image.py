# Generated by Django 5.0.4 on 2024-06-02 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='genre',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='genre_images/'),
        ),
    ]