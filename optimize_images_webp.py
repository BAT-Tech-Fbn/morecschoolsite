import os
import shutil
from PIL import Image
import time

# Configuration
JPEG_QUALITY = 70  # Qualité JPEG réduite (0-100)
WEBP_QUALITY = 75  # Qualité WebP (0-100)
MAX_WIDTH = 1600  # Largeur maximale réduite
CREATE_WEBP = True  # Créer des versions WebP en plus des originaux
BACKUP_DIR = "static/medias/backup_" + time.strftime("%Y%m%d_%H%M%S")

# Créer le répertoire de sauvegarde
os.makedirs(BACKUP_DIR, exist_ok=True)
print(f"Répertoire de sauvegarde créé : {BACKUP_DIR}")

# Extensions d'images supportées
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']

# Stats
total_files = 0
total_size_before = 0
total_size_after = 0
total_webp_size = 0

# Fonction pour optimiser une image
def optimize_image(image_path):
    global total_files, total_size_before, total_size_after, total_webp_size
    
    # Vérifier si c'est un fichier image
    file_ext = os.path.splitext(image_path)[1].lower()
    if file_ext not in image_extensions:
        return
    
    # Calculer le chemin de sauvegarde
    relative_path = os.path.relpath(image_path, "static/medias")
    backup_path = os.path.join(BACKUP_DIR, relative_path)
    
    # Créer le répertoire de sauvegarde si nécessaire
    os.makedirs(os.path.dirname(backup_path), exist_ok=True)
    
    # Sauvegarder l'image originale
    shutil.copy2(image_path, backup_path)
    
    # Obtenir la taille avant optimisation
    size_before = os.path.getsize(image_path)
    total_size_before += size_before
    
    try:
        # Ouvrir l'image
        with Image.open(image_path) as img:
            # Conserver le format original
            img_format = img.format
            
            # Redimensionner si nécessaire
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_width = MAX_WIDTH
                new_height = int(img.height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Sauvegarder l'image optimisée
            if img_format == 'JPEG' or file_ext in ['.jpg', '.jpeg']:
                img.save(image_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
            elif img_format == 'PNG' or file_ext == '.png':
                img.save(image_path, 'PNG', optimize=True, compress_level=9)
            else:
                # Pour les autres formats, conserver tel quel
                img.save(image_path, img_format)
            
            # Créer une version WebP si demandé
            if CREATE_WEBP:
                webp_path = os.path.splitext(image_path)[0] + '.webp'
                img.save(webp_path, 'WEBP', quality=WEBP_QUALITY)
                webp_size = os.path.getsize(webp_path)
                total_webp_size += webp_size
                print(f"Version WebP créée : {os.path.basename(webp_path)} ({webp_size/1024:.2f} KB)")
        
        # Obtenir la taille après optimisation
        size_after = os.path.getsize(image_path)
        total_size_after += size_after
        
        # Calculer la réduction en pourcentage
        reduction = (1 - size_after / size_before) * 100
        
        print(f"{os.path.basename(image_path)} : {size_before/1024:.2f} KB -> {size_after/1024:.2f} KB ({reduction:.2f}% réduit)")
        total_files += 1
        
    except Exception as e:
        print(f"Erreur lors de l'optimisation de {image_path}: {e}")

# Parcourir le répertoire des médias
media_dir = "static/medias"
for root, dirs, files in os.walk(media_dir):
    for file in files:
        file_path = os.path.join(root, file)
        # Ignorer les fichiers WebP existants et les fichiers de sauvegarde
        if file_path.endswith('.webp') or BACKUP_DIR in file_path:
            continue
        optimize_image(file_path)

# Afficher les statistiques
if total_files > 0:
    print("\n=== RÉSUMÉ ===")
    print(f"Images optimisées : {total_files}")
    print(f"Taille totale avant : {total_size_before/1024/1024:.2f} MB")
    print(f"Taille totale après : {total_size_after/1024/1024:.2f} MB")
    
    if CREATE_WEBP:
        print(f"Taille totale des WebP : {total_webp_size/1024/1024:.2f} MB")
        webp_reduction = (1 - total_webp_size / total_size_before) * 100
        print(f"Réduction avec WebP : {webp_reduction:.2f}%")
    
    print(f"Réduction totale : {(1 - total_size_after / total_size_before) * 100:.2f}%")
    print(f"Les images originales ont été sauvegardées dans : {BACKUP_DIR}")
    
    if CREATE_WEBP:
        print("\nPour utiliser les images WebP dans votre HTML, vous pouvez modifier vos balises img comme ceci:")
        print("""
<picture>
    <source srcset="chemin/vers/image.webp" type="image/webp">
    <img src="chemin/vers/image.jpg" alt="Description">
</picture>
        """)
else:
    print("Aucune image n'a été optimisée.")
