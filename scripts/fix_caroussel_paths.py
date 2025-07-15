import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MorecSchool.settings')
django.setup()
from core.models import CarousselImage

MEDIA_CAROUSSEL = 'caroussel/'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

fixed = 0
for img in CarousselImage.objects.all():
    if img.image and (not str(img.image).startswith(MEDIA_CAROUSSEL)):
        filename = os.path.basename(img.image.name)
        new_path = MEDIA_CAROUSSEL + filename
        full_path = os.path.join(MEDIA_ROOT, new_path)
        if os.path.exists(full_path):
            img.image.name = new_path
            img.save()
            fixed += 1
        else:
            print(f"[WARN] Fichier manquant pour {img.id}: {full_path}")
print(f"Corrigé {fixed} images carrousel.")
