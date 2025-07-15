from django.db import models

class Evenement(models.Model):
    titre = models.CharField(max_length=200)
    theme = models.CharField(max_length=200)
    frais = models.DecimalField(max_digits=8, decimal_places=2)
    affiche_evenement = models.ImageField(upload_to='affiches/', blank=True, null=True)

    def __str__(self):
        return f"{self.titre}"

class CarousselImage(models.Model):
    image = models.ImageField(upload_to='caroussel/')
    titre = models.CharField(max_length=255, blank=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titre or f"Image {self.id}"

class SliderImage(models.Model):
    image = models.ImageField(upload_to='slider/', help_text="Image pour le slider principal")
    image_webp = models.ImageField(upload_to='slider/', null=True, blank=True, help_text="Version WebP de l'image (optionnelle, sera générée automatiquement)")
    titre = models.CharField(max_length=100)
    sous_titre = models.CharField(max_length=200)
    texte_bouton = models.CharField(max_length=50, default="En savoir plus")
    url_bouton = models.CharField(max_length=200, default="#")
    ordre = models.PositiveSmallIntegerField(default=0, help_text="Ordre d'affichage des slides")
    actif = models.BooleanField(default=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordre', '-date_ajout']
        verbose_name = "Image du slider"
        verbose_name_plural = "Images du slider"
    
    def __str__(self):
        return self.titre

class EvenementDate(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='dates')
    date = models.DateField(verbose_name='Date')
    heure_debut = models.TimeField(verbose_name='Heure de début')
    heure_fin = models.TimeField(verbose_name='Heure de fin')

    def __str__(self):
        return f"{self.date} ({self.heure_debut}-{self.heure_fin})"

class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    approuve = models.BooleanField(default=False, verbose_name="Approuvé par l'admin")

    def __str__(self):
        return f"{self.nom} ({self.date})"

class Video(models.Model):
    titre = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    fichier = models.FileField(upload_to='static/medias/videos/', blank=True, null=True)
    pdf = models.FileField(upload_to='static/medias/pdfs/', blank=True, null=True, verbose_name='PDF associé')

    def __str__(self):
        return self.titre


from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
import uuid

class Animateur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    titre = models.CharField(max_length=200, help_text="Titre ou fonction de l'animateur")
    bio = models.TextField(blank=True, help_text="Courte biographie de l'animateur")
    photo = models.ImageField(upload_to='animateurs/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    class Meta:
        verbose_name = "Animateur"
        verbose_name_plural = "Animateurs"

class MasterClass(models.Model):
    theme = models.CharField(max_length=200, verbose_name="Thème du MasterClass")
    description = models.TextField(verbose_name="Résumé de description")
    date_creation = models.DateTimeField(default=timezone.now)
    date_debut = models.DateTimeField(blank=True, null=True, verbose_name="Date de début")
    date_fin = models.DateTimeField(blank=True, null=True, verbose_name="Date de fin")
    animateurs = models.ManyToManyField(Animateur, related_name='masterclasses')
    publie = models.BooleanField(default=False, verbose_name="Publié")
    
    def __str__(self):
        return self.theme
    
    class Meta:
        verbose_name = "MasterClass"
        verbose_name_plural = "MasterClasses"
        ordering = ['-date_creation']

class ImageMasterClass(models.Model):
    masterclass = models.ForeignKey(MasterClass, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='masterclass/images/')
    legende = models.CharField(max_length=255, blank=True)
    ordre = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Image MasterClass"
        verbose_name_plural = "Images MasterClass"

class VideoMasterClass(models.Model):
    masterclass = models.ForeignKey(MasterClass, on_delete=models.CASCADE, related_name='videos')
    titre = models.CharField(max_length=255)
    url = models.URLField(blank=True, help_text="URL YouTube ou autre plateforme (optionnel)")
    fichier = models.FileField(upload_to='masterclass/videos/', blank=True, null=True)
    description = models.TextField(blank=True)
    ordre = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Vidéo MasterClass"
        verbose_name_plural = "Vidéos MasterClass"
    
    def __str__(self):
        return self.titre

class UtilisateurEtendu(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    post = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    ETAT_CIVIL_CHOICES = [
        ('celibataire', 'Célibataire'),
        ('marie', 'Marié(e)'),
        ('divorce', 'Divorcé(e)'),
        ('veuf', 'Veuf/Veuve'),
    ]
    etat_civil = models.CharField(max_length=20, choices=ETAT_CIVIL_CHOICES)
    ville = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} {self.prenom}"


# Modèles pour la fonctionnalité Slido
class SessionInteractive(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    code = models.CharField(max_length=8, unique=True, editable=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions_creees')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    est_active = models.BooleanField(default=True)
    est_moderee = models.BooleanField(default=False, help_text="Si activé, les questions doivent être approuvées avant d'être visibles")
    
    def save(self, *args, **kwargs):
        # Génération d'un code unique si nouveau
        if not self.code:
            self.code = self.generate_unique_code()
            
        # Création du slug depuis le titre
        if not self.slug:
            self.slug = slugify(self.titre)
            
        super(SessionInteractive, self).save(*args, **kwargs)
    
    def generate_unique_code(self):
        """Génère un code court unique pour la session"""
        return str(uuid.uuid4())[:6].upper()
    
    def __str__(self):
        return f"{self.titre} ({self.code})"


class Question(models.Model):
    TYPE_CHOICES = [
        ('question', 'Question'),
        ('sondage', 'Sondage'),
        ('nuage', 'Nuage de mots'),
        ('quiz', 'Quiz')
    ]
    
    STATUS_CHOICES = [
        ('attente', 'En attente de modération'),
        ('approuvee', 'Approuvée'),
        ('rejetee', 'Rejetée')
    ]
    
    session = models.ForeignKey(SessionInteractive, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField()
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions_posees')
    anonyme = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='question')
    statut = models.CharField(max_length=10, choices=STATUS_CHOICES, default='attente')
    votes_positifs = models.PositiveIntegerField(default=0)
    est_repondue = models.BooleanField(default=False)
    est_epinglee = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-votes_positifs', '-date_creation']
    
    def __str__(self):
        return f"{self.texte[:50]}..."


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='votes')
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('question', 'utilisateur')
        
    def __str__(self):
        return f"Vote de {self.utilisateur} sur {self.question}"


class OptionSondage(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options', limit_choices_to={'type': 'sondage'})
    texte = models.CharField(max_length=255)
    votes = models.PositiveIntegerField(default=0)
    ordre = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return self.texte


class ReponseQuiz(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses_quiz', limit_choices_to={'type': 'quiz'})
    texte = models.CharField(max_length=255)
    est_correcte = models.BooleanField(default=False)
    ordre = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
    
    def __str__(self):
        return self.texte
