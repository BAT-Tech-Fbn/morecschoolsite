from PIL import Image
import os

# Configuration
JPEG_QUALITY = 65
WEBP_QUALITY = 75

# Fonction pour optimiser une seule image
def optimize_single_image(image_path):
    print(f"Optimisation de {image_path}")
    try:
        # Ouvrir et optimiser l'image
        img = Image.open(image_path)
        
        # Enregistrer en JPEG avec compression
        img.save(image_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        
        # Créer version WebP
        webp_path = os.path.splitext(image_path)[0] + '.webp'
        img.save(webp_path, 'WEBP', quality=WEBP_QUALITY)
        
        jpg_size = os.path.getsize(image_path) / 1024
        webp_size = os.path.getsize(webp_path) / 1024
        
        print(f"  JPEG: {jpg_size:.2f} KB, WebP: {webp_size:.2f} KB")
        return True
    except Exception as e:
        print(f"  Erreur: {e}")
        return False

# Optimiser des images spécifiques
images_to_optimize = [
    "static/medias/IMG-20250407-WA0160.jpg",
    "static/medias/Wonderful Creative-33.jpg",
    "static/medias/Wonderful Creative-41.jpg",
    "static/medias/Wonderful Creative-53.jpg", 
    "static/medias/Wonderful Creative-56.jpg",
    "static/medias/Wonderful Creative-90.jpg",
    "static/medias/WonderfulCreative-39.jpg"
]

successful = 0
for img_path in images_to_optimize:
    if os.path.exists(img_path):
        if optimize_single_image(img_path):
            successful += 1
    else:
        print(f"Fichier introuvable: {img_path}")

print(f"\nOptimisation terminée: {successful}/{len(images_to_optimize)} images traitées.")
