from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import UtilisateurEtendu, Evenement, EvenementDate, CarousselImage, Video, Temoignage, \
                  Animateur, MasterClass, ImageMasterClass, VideoMasterClass, SessionInteractive, \
                  Question, Vote, OptionSondage, ReponseQuiz

VILLE_CHOICES = [
    ('Kinshasa', 'Kinshasa'),
    ('Lubumbashi', 'Lubumbashi'),
    ('Goma', 'Goma'),
    ('Bukavu', 'Bukavu'),
    ('Kisangani', 'Kisangani'),
    ('Mbuji-Mayi', 'Mbuji-Mayi'),
    ('Kananga', 'Kananga'),
    ('Bunia', 'Bunia'),
    ('Matadi', 'Matadi'),
    ('Boma', 'Boma'),
    ('Uvira', 'Uvira'),
    # Ajoute d'autres villes importantes si besoin
]
SEXE_CHOICES = [
    ('M', 'Masculin'),
    ('F', 'Féminin'),
]

class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom d'utilisateur"}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}))
    ville = forms.ChoiceField(choices=VILLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = UtilisateurEtendu
        fields = ['nom', 'post', 'prenom', 'sexe', 'etat_civil', 'ville', 'numero_telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'post': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PostNom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'sexe': forms.Select(attrs={'class': 'form-control','placeholder': 'Sexe'}),
            'etat_civil': forms.Select(attrs={'class': 'form-control'}),
            'numero_telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Les mots de passe ne correspondent pas.')
        return cleaned_data

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
        )
        utilisateur = super().save(commit=False)
        utilisateur.user = user
        utilisateur.email = self.cleaned_data['email']
        if commit:
            utilisateur.save()
        return utilisateur



class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['titre', 'theme', 'frais', 'affiche_evenement']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Titre de l'événement"}),
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Thème'}),
            'frais': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Frais'}),
            'affiche_evenement': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CarousselImageForm(forms.ModelForm):
    class Meta:
        model = CarousselImage
        fields = ['image', 'titre']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre (optionnel)'}),
        }

class TemoignageForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None and user.is_authenticated:
            self.fields['nom'].widget = forms.HiddenInput()
            self.fields['nom'].required = False
    def clean_contenu(self):
        contenu = self.cleaned_data.get('contenu', '')
        if len(contenu) > 400:
            raise ValidationError('Le témoignage ne doit pas dépasser 400 caractères.')
        if len(contenu) < 20:
            raise ValidationError('Le témoignage doit contenir au moins 20 caractères.')
        return contenu
    class Meta:
        model = Temoignage
        fields = ['nom', 'contenu']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Votre témoignage', 'rows': 4, 'maxlength': '400'}),
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['titre', 'fichier', 'pdf']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la vidéo'}),
        }



class EvenementDateForm(forms.ModelForm):
    class Meta:
        model = EvenementDate
        fields = ['date', 'heure_debut', 'heure_fin']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Date'}),
            'heure_debut': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Heure de début'}),
            'heure_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Heure de fin'}),
        }

# Formulaires pour MasterClass
class AnimateurForm(forms.ModelForm):
    class Meta:
        model = Animateur
        fields = ['nom', 'prenom', 'titre', 'bio', 'photo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'animateur"}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Prénom de l'animateur"}),
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Titre ou fonction"}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Biographie", 'rows': 3}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class MasterClassForm(forms.ModelForm):
    class Meta:
        model = MasterClass
        fields = ['theme', 'description', 'date_debut', 'date_fin', 'animateurs', 'publie']
        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Thème du MasterClass"}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description détaillée", 'rows': 4}),
            'date_debut': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'date_fin': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'animateurs': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'publie': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ImageMasterClassForm(forms.ModelForm):
    class Meta:
        model = ImageMasterClass
        fields = ['image', 'legende', 'ordre']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'legende': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Légende de l'image"}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

class VideoMasterClassForm(forms.ModelForm):
    class Meta:
        model = VideoMasterClass
        fields = ['titre', 'url', 'fichier', 'description', 'ordre']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Titre de la vidéo"}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': "URL YouTube ou autre (optionnel)"}),
            'fichier': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Description", 'rows': 2}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }

# FormSets pour la gestion des images et vidéos liées à une MasterClass
ImageMasterClassFormSet = inlineformset_factory(
    MasterClass, 
    ImageMasterClass,
    form=ImageMasterClassForm,
    extra=1,
    can_delete=True
)

VideoMasterClassFormSet = inlineformset_factory(
    MasterClass, 
    VideoMasterClass,
    form=VideoMasterClassForm,
    extra=1,
    can_delete=True
)

# Formulaires pour la fonctionnalité Slido
class SessionInteractiveForm(forms.ModelForm):
    class Meta:
        model = SessionInteractive
        fields = ['titre', 'description', 'est_moderee']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de la session'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description de la session'}),
            'est_moderee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'est_moderee': 'Activer la modération des questions',
        }
        help_texts = {
            'titre': 'Un titre court et descriptif pour la session',
            'description': 'Informations sur le but de cette session interactive',
            'est_moderee': 'Si activé, les questions devront être approuvées avant d\'être visibles par tous',
        }

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Extraire session et user des kwargs
        self.session = kwargs.pop('session', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Limiter les types disponibles pour les utilisateurs non-staff
        if not self.user or not self.user.is_staff:
            self.fields['type'].choices = [('question', 'Question')]
            self.fields['type'].widget = forms.HiddenInput()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.session:
            instance.session = self.session
        if self.user and not instance.anonyme:
            instance.auteur = self.user
            
        # Si la session est modérée et l'utilisateur n'est pas staff, mettre en attente
        if self.session and self.session.est_moderee and not self.user.is_staff:
            instance.statut = 'attente'
        else:
            instance.statut = 'approuvee'
            
        if commit:
            instance.save()
        return instance
    
    class Meta:
        model = Question
        fields = ['texte', 'type', 'anonyme']
        widgets = {
            'texte': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Posez votre question ici...'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'anonyme': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'anonyme': 'Rester anonyme',
            'texte': 'Votre question',
            'type': 'Type de question',
        }
        help_texts = {
            'type': 'Le type de question que vous souhaitez poser',
            'anonyme': 'Si activé, votre nom ne sera pas affiché avec la question',
        }

class CodeSessionForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Entrez le code de la session',
            'aria-label': 'Code de session',
        }),
        help_text='Le code à 6 chiffres fourni par l\'organisateur',
        error_messages={
            'required': 'Veuillez entrer un code de session.',
            'min_length': 'Le code doit contenir au moins 6 caractères.',
            'max_length': 'Le code ne peut pas dépasser 8 caractères.',
        }
    )
    
    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Vérifier si le code correspond à une session existante
            try:
                session = SessionInteractive.objects.get(code=code)
                return code
            except SessionInteractive.DoesNotExist:
                raise forms.ValidationError("Aucune session ne correspond à ce code.")
        return code

class OptionSondageForm(forms.ModelForm):
    class Meta:
        model = OptionSondage
        fields = ['texte']
        widgets = {
            'texte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option de réponse'}),
        }
        labels = {'texte': ''}

OptionSondageFormSet = inlineformset_factory(
    Question, 
    OptionSondage,
    form=OptionSondageForm,
    extra=2,
    min_num=2,
    validate_min=True,
    can_delete=True
)

class ReponseQuizForm(forms.ModelForm):
    class Meta:
        model = ReponseQuiz
        fields = ['texte', 'est_correcte']
        widgets = {
            'texte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Réponse'}),
            'est_correcte': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'texte': '',
            'est_correcte': 'Correcte',
        }

ReponseQuizFormSet = inlineformset_factory(
    Question,
    ReponseQuiz,
    form=ReponseQuizForm,
    extra=4,
    min_num=2,
    validate_min=True,
    can_delete=True
)

class CodeSessionForm(forms.Form):
    code = forms.CharField(
        max_length=8, 
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center', 
            'placeholder': 'Entrez le code de session', 
            'autocomplete': 'off',
            'style': 'font-size: 1.5rem; letter-spacing: 0.5rem;'
        })
    )
    
    def clean_code(self):
        code = self.cleaned_data['code'].strip().upper()
        try:
            session = SessionInteractive.objects.get(code=code, est_active=True)
        except SessionInteractive.DoesNotExist:
            raise forms.ValidationError('Code de session invalide ou session inactive')
        return code
