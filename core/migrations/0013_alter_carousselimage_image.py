# Generated by Django 5.0 on 2025-06-21 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_evenement_affiche_evenement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousselimage',
            name='image',
            field=models.ImageField(upload_to='caroussel/'),
        ),
    ]
