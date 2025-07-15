import os
from PIL import Image

# Configuration
JPEG_QUALITY = 65  # Qualité JPEG encore plus réduite (0-100)
WEBP_QUALITY = 75  # Qualité WebP (0-100)
MAX_WIDTH = 1600   # Largeur maximale

# Liste des images à optimiser
image_files = [
    "static/medias/banniere-accueil.jpg",
    "static/medias/IMG-20250119-WA0004.jpg",
    "static/medias/IMG-20250407-WA0160.jpg",
    "static/medias/Wonderful Creative-33.jpg",
    "static/medias/Wonderful Creative-41.jpg",
    "static/medias/Wonderful Creative-53.jpg",
    "static/medias/Wonderful Creative-56.jpg",
    "static/medias/Wonderful Creative-90.jpg",
    "static/medias/WonderfulCreative-39.jpg"
]

# Optimisation des images
for image_path in image_files:
    if not os.path.exists(image_path):
        print(f"Fichier non trouvé : {image_path}")
        continue
        
    print(f"Traitement de {image_path}...")
    size_before = os.path.getsize(image_path) / 1024  # KB
    
    try:
        # Ouvrir l'image
        with Image.open(image_path) as img:
            # Redimensionner si nécessaire
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_width = MAX_WIDTH
                new_height = int(img.height * ratio)
                print(f"  Redimensionnement : {img.width}x{img.height} -> {new_width}x{new_height}")
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Sauvegarder l'image optimisée
            img.save(image_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            
            # Créer une version WebP
            webp_path = os.path.splitext(image_path)[0] + '.webp'
            img.save(webp_path, 'WEBP', quality=WEBP_QUALITY)
            webp_size = os.path.getsize(webp_path) / 1024  # KB
            print(f"  Version WebP créée : {os.path.basename(webp_path)} ({webp_size:.2f} KB)")
        
        # Obtenir la taille après optimisation
        size_after = os.path.getsize(image_path) / 1024  # KB
        reduction = (1 - size_after / size_before) * 100
        print(f"  {os.path.basename(image_path)} : {size_before:.2f} KB -> {size_after:.2f} KB ({reduction:.2f}% réduit)")
        
    except Exception as e:
        print(f"  Erreur lors de l'optimisation de {image_path}: {e}")

print("\nToutes les images ont été traitées.")
print("\nPour utiliser les images WebP dans votre site Django, modifiez vos templates ainsi :")
print("""
{% load static %}
<picture>
    <source srcset="{% static 'medias/nom-image.webp' %}" type="image/webp">
    <img src="{% static 'medias/nom-image.jpg' %}" alt="Description de l'image">
</picture>
""")
