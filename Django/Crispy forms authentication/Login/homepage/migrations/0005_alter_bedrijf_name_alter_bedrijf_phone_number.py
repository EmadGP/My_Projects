# Generated by Django 4.2.7 on 2024-01-02 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0004_bedrijf_stageperiode_bedrijf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bedrijf',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='bedrijf',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
