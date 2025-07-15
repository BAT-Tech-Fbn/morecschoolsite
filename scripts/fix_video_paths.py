import os
import django
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MorecSchool.settings')
django.setup()
from core.models import Video

MEDIA_VIDEOS = 'videos/'
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'media')

fixed = 0
for vid in Video.objects.all():
    if vid.fichier and (not str(vid.fichier).startswith(MEDIA_VIDEOS)):
        filename = os.path.basename(vid.fichier.name)
        new_path = MEDIA_VIDEOS + filename
        full_path = os.path.join(MEDIA_ROOT, new_path)
        if os.path.exists(full_path):
            vid.fichier.name = new_path
            vid.save()
            fixed += 1
        else:
            print(f"[WARN] Fichier manquant pour {vid.id}: {full_path}")
print(f"Corrigé {fixed} vidéos.")
