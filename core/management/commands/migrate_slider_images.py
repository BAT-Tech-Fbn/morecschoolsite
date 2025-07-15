from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import SliderImage
import os
from django.conf import settings
import shutil
from pathlib import Path
from django.contrib.staticfiles.storage import staticfiles_storage

class Command(BaseCommand):
    help = 'Migrer les images existantes du slider vers le nouveau modèle SliderImage'

    def handle(self, *args, **options):
        # Données pour les slides existants
        slides = [
            {
                'image': 'medias/IMG-20250407-WA0160.jpg',
                'image_webp': 'medias/IMG-20250407-WA0160.webp',
                'titre': 'Bienvenue à MOREC SCHOOL',
                'sous_titre': 'Développez votre leadership avec nous',
                'texte_bouton': 'Rejoindre notre communauté',
                'url_bouton': '/register/',
                'ordre': 1
            },
            {
                'image': 'medias/WonderfulCreative-39.jpg',
                'image_webp': 'medias/WonderfulCreative-39.webp',
                'titre': 'ÉQUIPER LES LEADERS D\'AUJOURD\'HUI ET DE DEMAIN',
                'sous_titre': 'Nous formons les leaders de toutes tendances',
                'texte_bouton': 'Découvrir les programmes',
                'url_bouton': '/cours/',
                'ordre': 2
            },
            {
                'image': 'medias/Wonderful Creative-33.jpg',
                'image_webp': 'medias/Wonderful Creative-33.webp',
                'titre': 'Construisons une génération de leaders',
                'sous_titre': 'Chaque leader éclairé transforme sa communauté.',
                'texte_bouton': 'Faire un don ou devenir un partenaire',
                'url_bouton': '#',
                'ordre': 3
            }
        ]

        # Vérifier si des slides existent déjà
        if SliderImage.objects.exists():
            self.stdout.write(self.style.WARNING('Des images de slider existent déjà dans la base de données. Voulez-vous continuer et ajouter ces images ? (o/n)'))
            answer = input().lower()
            if answer != 'o' and answer != 'oui':
                self.stdout.write(self.style.WARNING('Migration annulée.'))
                return

        count = 0
        for slide_data in slides:
            # Chemin source des images
            static_path = os.path.join(settings.BASE_DIR, 'static')
            source_path = os.path.join(static_path, slide_data['image'])
            source_path_webp = os.path.join(static_path, slide_data['image_webp'])
            
            # Vérifier si les fichiers existent
            if not os.path.exists(source_path):
                self.stdout.write(self.style.WARNING(f"L'image {source_path} n'existe pas. Ignorer ce slide."))
                continue
                
            # Créer un dossier pour les images du slider s'il n'existe pas
            media_root = settings.MEDIA_ROOT
            slider_dir = os.path.join(media_root, 'slider')
            os.makedirs(slider_dir, exist_ok=True)
            
            # Chemin de destination des images
            filename = os.path.basename(source_path)
            filename_webp = os.path.basename(source_path_webp)
            
            # Copier l'image vers le dossier media/slider
            dest_path = os.path.join(slider_dir, filename)
            dest_path_webp = os.path.join(slider_dir, filename_webp)
            
            # Copier les fichiers (si nécessaire)
            shutil.copy2(source_path, dest_path)
            has_webp = os.path.exists(source_path_webp)
            if has_webp:
                shutil.copy2(source_path_webp, dest_path_webp)
            
            # Créer l'instance SliderImage
            slider = SliderImage()
            slider.titre = slide_data['titre']
            slider.sous_titre = slide_data['sous_titre']
            slider.texte_bouton = slide_data['texte_bouton']
            slider.url_bouton = slide_data['url_bouton']
            slider.ordre = slide_data['ordre']
            
            # Définir les images
            with open(dest_path, 'rb') as img_file:
                slider.image.save(filename, File(img_file), save=False)
            
            if has_webp:
                with open(dest_path_webp, 'rb') as webp_file:
                    slider.image_webp.save(filename_webp, File(webp_file), save=False)
            
            slider.save()
            count += 1
            
        self.stdout.write(self.style.SUCCESS(f'{count} images ont été migrées avec succès.'))
