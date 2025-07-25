# Generated by Django 5.0 on 2025-06-21 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_carousselimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='fichier',
            field=models.FileField(blank=True, null=True, upload_to='static/medias/videos/'),
        ),
        migrations.AlterField(
            model_name='carousselimage',
            name='image',
            field=models.ImageField(upload_to='static/medias/caroussel/'),
        ),
        migrations.AlterField(
            model_name='video',
            name='titre',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
