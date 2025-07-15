from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from .models import Evenement, Temoignage, Video, UtilisateurEtendu, EvenementDate, CarousselImage, SliderImage, \
                   Animateur, MasterClass, ImageMasterClass, VideoMasterClass, \
                   SessionInteractive, Question, Vote, OptionSondage, ReponseQuiz

from django.core.paginator import Paginator

def home(request):
    from .forms import TemoignageForm, CodeSessionForm
    # Récupération des témoignages pour la pagination
    temoignages_qs = Temoignage.objects.filter(approuve=True).order_by('-date')
    paginator = Paginator(temoignages_qs, 3)
    page_number = request.GET.get('page')
    temoignages_page = paginator.get_page(page_number)
    
    # Récupération des vidéos et images pour le carrousel
    videos = Video.objects.exclude(fichier='').order_by('-id')[:3]
    caroussel_images = CarousselImage.objects.all().order_by('-date_ajout')
    slider_images = SliderImage.objects.filter(actif=True)
    
    # Récupération des sessions interactives actives
    sessions_actives = SessionInteractive.objects.filter(est_active=True).order_by('-date_creation')[:3]
    code_session_form = CodeSessionForm()
    
    # Gestion du formulaire de témoignage
    temoignage_form = TemoignageForm(user=request.user)
    message = None
    if request.method == 'POST' and 'temoignage-submit' in request.POST:
        if not request.user.is_authenticated:
            message = "Vous devez être connecté pour laisser un témoignage."
        else:
            post_data = request.POST.copy()
            post_data['nom'] = request.user.get_full_name() or request.user.username
            temoignage_form = TemoignageForm(post_data, user=request.user)
            if temoignage_form.is_valid():
                temoignage_form.save()
                message = "Merci pour votre témoignage ! Il sera affiché après validation."
                temoignage_form = TemoignageForm(user=request.user)  # reset
    return render(request, 'home.html', {
        'temoignages': temoignages_page,
        'videos': videos,
        'caroussel_images': caroussel_images,
        'slider_images': slider_images,
        'temoignage_form': temoignage_form,
        'temoignage_message': message,
        'is_paginated': paginator.num_pages > 1,
        'sessions_actives': sessions_actives,
        'code_session_form': code_session_form,
        'page_obj': temoignages_page,
    })

def gestion_temoignages(request):
    from django.contrib.admin.views.decorators import staff_member_required
    from django.utils.decorators import method_decorator
    if not request.user.is_staff:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Accès réservé à l'administrateur.")
    if request.method == 'POST':
        tid = request.POST.get('temoignage_id')
        action = request.POST.get('action')
        if tid and action:
            t = Temoignage.objects.get(id=tid)
            if action == 'approuver':
                t.approuve = True
                t.save()
            elif action == 'supprimer':
                t.delete()
    temoignages = Temoignage.objects.all().order_by('-date')
    return render(request, 'gestion_temoignages.html', {'temoignages': temoignages})

from django.utils import timezone
from .forms import RegisterForm

def evenements(request):
    from django.db.models import Min
    today = timezone.now().date()
    # Annoter chaque événement avec sa date la plus proche
    evenements = Evenement.objects.annotate(
        prochaine_date=Min('dates__date')
    ).filter(dates__date__gte=today).order_by('prochaine_date')
    return render(request, 'evenements.html', {'evenements': evenements})

def a_propos(request):
    return render(request, 'a_propos.html')

def connexion(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'connexion.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST)
        if reg_form.is_valid():
            utilisateur = reg_form.save()
            login(request, utilisateur.user)
            return redirect('home')
    else:
        reg_form = RegisterForm()
    return render(request, 'register.html', {'reg_form': reg_form})

def deconnexion(request):
    logout(request)
    return redirect('home')


def membres(request):
    membres = UtilisateurEtendu.objects.all()
    return render(request, 'membres.html', {'membres': membres})

from .forms import RegisterForm, EvenementForm, EvenementDateForm, MasterClassForm, AnimateurForm, \
                 ImageMasterClassFormSet, VideoMasterClassFormSet
from django.forms import modelformset_factory

def gestion_evenements(request):
    evenements = Evenement.objects.all().order_by('-id')
    return render(request, 'gestion_evenements.html', {'evenements': evenements})

def modifier_evenement(request, event_id):
    evenement = Evenement.objects.get(id=event_id)
    EvenementDateFormSet = modelformset_factory(EvenementDate, form=EvenementDateForm, extra=0, can_delete=True)
    if request.method == 'POST':
        event_form = EvenementForm(request.POST, instance=evenement)
        formset = EvenementDateFormSet(request.POST, queryset=EvenementDate.objects.filter(evenement=evenement))
        if event_form.is_valid() and formset.is_valid():
            event_form.save()
            for form in formset:
                if form.cleaned_data:
                    if form.cleaned_data.get('DELETE', False):
                        if form.instance.pk:
                            form.instance.delete()
                    else:
                        date_obj = form.save(commit=False)
                        date_obj.evenement = evenement
                        date_obj.save()
            return redirect('gestion_evenements')
    else:
        event_form = EvenementForm(instance=evenement)
        formset = EvenementDateFormSet(queryset=EvenementDate.objects.filter(evenement=evenement))
    return render(request, 'ajouter_evenement.html', {'form': event_form, 'formset': formset, 'modifier': True})

def supprimer_evenement(request, event_id):
    evenement = Evenement.objects.get(id=event_id)
    evenement.delete()
    return redirect('gestion_evenements')

def modifier_caroussel_image(request, image_id):
    img = CarousselImage.objects.get(id=image_id)
    from .forms import CarousselImageForm
    if request.method == 'POST':
        form = CarousselImageForm(request.POST, instance=img)
        if form.is_valid():
            form.save()
            return redirect('enregistrer_caroussel_image')
    else:
        form = CarousselImageForm(instance=img)
    # On ne montre que le champ titre
    form.fields.pop('image')
    return render(request, 'modifier_caroussel_image.html', {'form': form, 'image': img})

def supprimer_caroussel_image(request, image_id):
    if request.method == 'POST':
        img = CarousselImage.objects.get(id=image_id)
        img.delete()
    return redirect('enregistrer_caroussel_image')

def modifier_video(request, video_id):
    from .forms import VideoForm
    video = Video.objects.get(id=video_id)
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('enregistrer_video')
    else:
        form = VideoForm(instance=video)
    return render(request, 'modifier_video.html', {'form': form, 'video': video})

def supprimer_video(request, video_id):
    if request.method == 'POST':
        video = Video.objects.get(id=video_id)
        video.delete()
    return redirect('enregistrer_video')

from django.forms import modelformset_factory

def enregistrer_video(request):
    from .forms import VideoForm
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('enregistrer_video')
    else:
        form = VideoForm()
    videos = Video.objects.exclude(fichier='').order_by('-id')
    return render(request, 'enregistrer_video.html', {'form': form, 'videos': videos})

@login_required
def reglage(request):
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('home')
    return render(request, 'reglage.html')

@login_required
def gestion_utilisateurs(request):
    """Afficher et gérer la liste des utilisateurs enregistrés"""
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('home')
    
    # Récupérer tous les utilisateurs sauf l'administrateur actuel
    users = User.objects.exclude(id=request.user.id).order_by('date_joined')
    return render(request, 'gestion_utilisateurs.html', {
        'users': users
    })

def enregistrer_caroussel_image(request):
    from .forms import CarousselImageForm
    if request.method == 'POST':
        form = CarousselImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('enregistrer_caroussel_image')
    else:
        form = CarousselImageForm()
    images = CarousselImage.objects.all().order_by('-date_ajout')
    return render(request, 'enregistrer_caroussel_image.html', {'form': form, 'images': images})

@login_required
def ajouter_evenement(request):
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('evenements')
    
    EvenementDateFormSet = modelformset_factory(EvenementDateForm._meta.model, form=EvenementDateForm, extra=1, can_delete=True)
    if request.method == 'POST':
        event_form = EvenementForm(request.POST, request.FILES)
        formset = EvenementDateFormSet(request.POST, queryset=EvenementDate.objects.none())
        if event_form.is_valid() and formset.is_valid():
            evenement = event_form.save()
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    date_obj = form.save(commit=False)
                    date_obj.evenement = evenement
                    date_obj.save()
            return redirect('evenements')
    else:
        event_form = EvenementForm()
        formset = EvenementDateFormSet(queryset=EvenementDate.objects.none())
    return render(request, 'ajouter_evenement.html', {'form': event_form, 'formset': formset})

# Create your views here.

# Vues pour l'affichage public des MasterClasses
def masterclasses_publiques(request):
    """Afficher la liste des MasterClasses au public"""
    masterclasses = MasterClass.objects.all().order_by('-date_creation')
    return render(request, 'masterclass_publiques.html', {
        'masterclasses': masterclasses
    })

# Vues pour la gestion des MasterClasses
@login_required
def liste_masterclasses(request):
    """Afficher la liste des MasterClasses"""
    masterclasses = MasterClass.objects.all().order_by('-date_creation')
    return render(request, 'masterclass/liste.html', {
        'masterclasses': masterclasses
    })

@login_required
def detail_masterclass(request, masterclass_id):
    """Afficher les détails d'une MasterClass"""
    masterclass = get_object_or_404(MasterClass, id=masterclass_id)
    return render(request, 'masterclass/detail.html', {
        'masterclass': masterclass
    })

@login_required
def ajouter_masterclass(request):
    """Ajouter une nouvelle MasterClass avec ses images et vidéos"""
    if request.method == 'POST':
        form = MasterClassForm(request.POST)
        if form.is_valid():
            masterclass = form.save()
            
            # Traiter les formsets pour les images
            image_formset = ImageMasterClassFormSet(request.POST, request.FILES, instance=masterclass)
            if image_formset.is_valid():
                image_formset.save()
            
            # Traiter les formsets pour les vidéos
            video_formset = VideoMasterClassFormSet(request.POST, request.FILES, instance=masterclass)
            if video_formset.is_valid():
                video_formset.save()
            
            messages.success(request, 'MasterClass ajoutée avec succès')
            return redirect('liste_masterclasses')
    else:
        form = MasterClassForm()
        image_formset = ImageMasterClassFormSet()
        video_formset = VideoMasterClassFormSet()
    
    animateurs = Animateur.objects.all()
    
    return render(request, 'masterclass/ajouter.html', {
        'form': form,
        'image_formset': image_formset,
        'video_formset': video_formset,
        'animateurs': animateurs
    })

@login_required
def modifier_masterclass(request, masterclass_id):
    """Modifier une MasterClass existante avec ses images et vidéos"""
    masterclass = get_object_or_404(MasterClass, id=masterclass_id)
    
    if request.method == 'POST':
        form = MasterClassForm(request.POST, instance=masterclass)
        if form.is_valid():
            masterclass = form.save()
            
            # Traiter les formsets pour les images
            image_formset = ImageMasterClassFormSet(request.POST, request.FILES, instance=masterclass)
            if image_formset.is_valid():
                image_formset.save()
            
            # Traiter les formsets pour les vidéos
            video_formset = VideoMasterClassFormSet(request.POST, request.FILES, instance=masterclass)
            if video_formset.is_valid():
                video_formset.save()
            
            messages.success(request, 'MasterClass modifiée avec succès')
            return redirect('detail_masterclass', masterclass_id=masterclass.id)
    else:
        form = MasterClassForm(instance=masterclass)
        image_formset = ImageMasterClassFormSet(instance=masterclass)
        video_formset = VideoMasterClassFormSet(instance=masterclass)
    
    animateurs = Animateur.objects.all()
    
    return render(request, 'masterclass/modifier.html', {
        'form': form,
        'masterclass': masterclass,
        'image_formset': image_formset,
        'video_formset': video_formset,
        'animateurs': animateurs
    })

@login_required
def supprimer_masterclass(request, masterclass_id):
    """Supprimer une MasterClass"""
    masterclass = get_object_or_404(MasterClass, id=masterclass_id)
    
    if request.method == 'POST':
        masterclass.delete()
        messages.success(request, 'MasterClass supprimée avec succès')
        return redirect('liste_masterclasses')
    
    return render(request, 'masterclass/supprimer.html', {
        'masterclass': masterclass
    })

@login_required
def ajouter_animateur(request):
    """Ajouter un nouvel animateur"""
    if request.method == 'POST':
        form = AnimateurForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animateur ajouté avec succès')
            return redirect('liste_animateurs')
    else:
        form = AnimateurForm()
    
    return render(request, 'masterclass/ajouter_animateur.html', {
        'form': form
    })

@login_required
def liste_animateurs(request):
    """Afficher la liste des animateurs"""
    animateurs = Animateur.objects.all().order_by('nom', 'prenom')
    return render(request, 'masterclass/liste_animateurs.html', {
        'animateurs': animateurs
    })

@login_required
def detail_animateur(request, animateur_id):
    """Afficher les détails d'un animateur"""
    animateur = get_object_or_404(Animateur, id=animateur_id)
    return render(request, 'masterclass/detail_animateur.html', {
        'animateur': animateur
    })

@login_required
def modifier_animateur(request, animateur_id):
    """Modifier un animateur existant"""
    animateur = get_object_or_404(Animateur, id=animateur_id)
    
    if request.method == 'POST':
        form = AnimateurForm(request.POST, request.FILES, instance=animateur)
        if form.is_valid():
            form.save()
            messages.success(request, 'Animateur modifié avec succès')
            return redirect('liste_animateurs')
    else:
        form = AnimateurForm(instance=animateur)
    
    return render(request, 'masterclass/modifier_animateur.html', {
        'form': form,
        'animateur': animateur
    })

@login_required
def supprimer_animateur(request, animateur_id):
    """Supprimer un animateur"""
    animateur = get_object_or_404(Animateur, id=animateur_id)
    
    if request.method == 'POST':
        animateur.delete()
        messages.success(request, 'Animateur supprimé avec succès')
        return redirect('liste_animateurs')
    
    return render(request, 'masterclass/supprimer_animateur.html', {
        'animateur': animateur
    })

def cours_list(request):
    videos = Video.objects.exclude(fichier='').order_by('-id')
    cours = None
    cours_id = request.GET.get('cours')
    corrections = []  # liste des quiz.id où la réponse utilisateur est fausse
    score = None
    total = 0
    bonnes = 0
    if cours_id:
        try:
            cours = Video.objects.get(id=cours_id)
        except Video.DoesNotExist:
            cours = None
    user_answers = {}
    if cours and request.method == 'POST':
        for quiz in cours.quiz_questions.all():
            user_answer = request.POST.get(f'reponse_{quiz.id}', '').strip()
            user_answers[quiz.id] = user_answer
            if quiz.reponse:
                total += 1
                # Vérification stricte (insensible à la casse et espaces)
                if user_answer.lower().strip() == quiz.reponse.lower().strip():
                    bonnes += 1
                else:
                    corrections.append(str(quiz.id))
        score = {'bonnes': bonnes, 'total': total}
    return render(request, 'cours.html', {'videos': videos, 'cours': cours, 'corrections': corrections, 'score': score, 'user_answers': user_answers})


# Vues pour la fonctionnalité Slido
from .forms import SessionInteractiveForm, QuestionForm, OptionSondageFormSet, ReponseQuizFormSet, CodeSessionForm


def accueil_interactive(request):
    """Page d'accueil pour la fonctionnalité interactive (type Slido)"""
    # Récupération de toutes les sessions actives
    sessions_actives = SessionInteractive.objects.filter(est_active=True).order_by('-date_creation')
    
    form = CodeSessionForm()
    message = None
    
    # Traitement du formulaire de code de session
    if request.method == 'POST':
        form = CodeSessionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                session = SessionInteractive.objects.get(code=code)
                # Rediriger vers la session correspondante
                return redirect('session_interactive', session_slug=session.slug)
            except SessionInteractive.DoesNotExist:
                message = "Aucune session ne correspond à ce code."
        else:
            # En cas d'erreurs dans le formulaire
            message = "Veuillez vérifier le code saisi."
    
    # Récupération des statistiques pour la page d'accueil
    total_sessions = SessionInteractive.objects.count()
    total_questions = Question.objects.count()
    total_votes = sum(q.votes.count() for q in Question.objects.all())
    
    return render(request, 'interactive/accueil.html', {
        'form': form,
        'sessions_actives': sessions_actives,
        'message': message,
        'stats': {
            'sessions': total_sessions,
            'questions': total_questions,
            'votes': total_votes,
        },
        'recent_sessions': SessionInteractive.objects.order_by('-date_creation')[:5]
    })


@login_required
def creer_session(request):
    """Créer une nouvelle session interactive"""
    if not request.user.is_staff:
        messages.error(request, "Vous n'avez pas l'autorisation de créer une session.")
        return redirect('accueil_interactive')
        
    if request.method == 'POST':
        form = SessionInteractiveForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.createur = request.user
            session.save()
            messages.success(request, f"Session '{session.titre}' créée avec succès ! Code: {session.code}")
            return redirect('gestion_session', session_slug=session.slug)
    else:
        form = SessionInteractiveForm()
    
    return render(request, 'interactive/creer_session.html', {'form': form})


def session_interactive(request, session_slug):
    """Affichage et interaction avec une session interactive"""
    session = get_object_or_404(SessionInteractive, slug=session_slug, est_active=True)
    questions = session.questions.filter(Q(statut='approuvee') | Q(auteur=request.user if request.user.is_authenticated else None))
    
    # Pour le tri et la pagination
    sort = request.GET.get('sort', '-votes_positifs')
    if sort not in ['-votes_positifs', '-date_creation', 'date_creation']:
        sort = '-votes_positifs'
    
    questions = questions.order_by('-est_epinglee', sort)
    
    # Formulaire pour poser une question
    question_form = None
    if request.user.is_authenticated:
        if request.method == 'POST' and 'submit_question' in request.POST:
            question_form = QuestionForm(request.POST, session=session, user=request.user)
            if question_form.is_valid():
                question = question_form.save()
                if session.est_moderee and not request.user.is_staff:
                    messages.info(request, "Votre question a été soumise et est en attente de modération.")
                else:
                    # Approuver automatiquement si pas de modération ou si c'est un staff
                    question.statut = 'approuvee'
                    question.save()
                return redirect('session_interactive', session_slug=session.slug)
        else:
            question_form = QuestionForm(session=session, user=request.user)
    
    return render(request, 'interactive/session.html', {
        'session': session,
        'questions': questions,
        'question_form': question_form,
        'sort': sort
    })


@login_required
def gestion_session(request, session_slug):
    """Gestion d'une session interactive (modération, configuration)"""
    session = get_object_or_404(SessionInteractive, slug=session_slug)
    
    # Vérifier que l'utilisateur est le créateur ou un admin
    if session.createur != request.user and not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les permissions pour gérer cette session.")
        return redirect('accueil_interactive')
    
    # Questions en attente de modération
    questions_attente = session.questions.filter(statut='attente').order_by('date_creation')
    
    # Toutes les questions
    toutes_questions = session.questions.all().order_by('-est_epinglee', '-votes_positifs', '-date_creation')
    
    # Modification des paramètres de la session
    if request.method == 'POST' and 'update_session' in request.POST:
        form = SessionInteractiveForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres de la session mis à jour.")
            return redirect('gestion_session', session_slug=session.slug)
    else:
        form = SessionInteractiveForm(instance=session)
    
    return render(request, 'interactive/gestion_session.html', {
        'session': session,
        'form': form,
        'questions_attente': questions_attente,
        'toutes_questions': toutes_questions
    })


@login_required
def approuver_question(request, question_id):
    """Approuver une question en attente"""
    question = get_object_or_404(Question, id=question_id)
    
    # Vérifier les permissions
    if question.session.createur != request.user and not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les permissions pour cette action.")
        return redirect('session_interactive', session_slug=question.session.slug)
    
    question.statut = 'approuvee'
    question.save()
    messages.success(request, "Question approuvée.")
    return redirect('gestion_session', session_slug=question.session.slug)


@login_required
def rejeter_question(request, question_id):
    """Rejeter une question en attente"""
    question = get_object_or_404(Question, id=question_id)
    
    # Vérifier les permissions
    if question.session.createur != request.user and not request.user.is_staff:
        messages.error(request, "Vous n'avez pas les permissions pour cette action.")
        return redirect('session_interactive', session_slug=question.session.slug)
    
    question.statut = 'rejetee'
    question.save()
    messages.success(request, "Question rejetée.")
    return redirect('gestion_session', session_slug=question.session.slug)


@csrf_exempt
def voter_question(request, question_id):
    """API pour voter pour une question (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Non autorisé"}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    
    question = get_object_or_404(Question, id=question_id)
    
    # Vérifier si l'utilisateur a déjà voté
    vote_existant = Vote.objects.filter(question=question, utilisateur=request.user).exists()
    
    if vote_existant:
        # Retirer le vote
        Vote.objects.filter(question=question, utilisateur=request.user).delete()
        question.votes_positifs = Vote.objects.filter(question=question).count()
        question.save()
        return JsonResponse({"votes": question.votes_positifs, "action": "retiré"})
    else:
        # Ajouter le vote
        Vote.objects.create(question=question, utilisateur=request.user)
        question.votes_positifs = Vote.objects.filter(question=question).count()
        question.save()
        return JsonResponse({"votes": question.votes_positifs, "action": "ajouté"})


@csrf_exempt
def epingler_question(request, question_id):
    """API pour épingler/désépingler une question (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Non autorisé"}, status=401)
    
    question = get_object_or_404(Question, id=question_id)
    session = question.session
    
    # Vérifier les permissions
    if session.createur != request.user and not request.user.is_staff:
        return JsonResponse({"error": "Permissions insuffisantes"}, status=403)
    
    # Inverser l'état épinglé
    question.est_epinglee = not question.est_epinglee
    question.save()
    
    return JsonResponse({"est_epinglee": question.est_epinglee})


@csrf_exempt
def marquer_repondue(request, question_id):
    """API pour marquer une question comme répondue (AJAX)"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Non autorisé"}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({"error": "Méthode non autorisée"}, status=405)
    
    question = get_object_or_404(Question, id=question_id)
    
    # Vérifier les permissions
    if question.session.createur != request.user and not request.user.is_staff:
        return JsonResponse({"error": "Vous n'avez pas les permissions pour cette action"}, status=403)
    
    # Basculer l'état de réponse
    question.est_repondue = not question.est_repondue
    question.save()
    
    return JsonResponse({
        "success": True,
        "est_repondue": question.est_repondue,
    })


def session_questions_json(request, session_slug):
    """API JSON pour récupérer les questions d'une session (pour le rafraîchissement automatique)"""
    from django.http import JsonResponse
    from django.utils.timesince import timesince
    from django.db.models import Count
    
    # Récupérer la session
    session = get_object_or_404(SessionInteractive, slug=session_slug)
    
    # Vérifier si l'utilisateur peut accéder à la session
    if not session.est_active and not (request.user.is_authenticated and (request.user.is_staff or request.user == session.createur)):
        return JsonResponse({'error': 'Session non accessible'}, status=403)
    
    # Récupérer les questions approuvées
    questions = session.questions.filter(statut='approuvee').annotate(votes_count=Count('votes')).order_by('-est_epinglee', '-votes_count', '-date_creation')
    
    # Formater les questions pour le JSON
    questions_data = []
    for question in questions:
        # Déterminer si l'utilisateur a déjà voté pour cette question
        user_has_voted = False
        if request.user.is_authenticated:
            user_has_voted = question.votes.filter(id=request.user.id).exists()
        
        # Déterminer si l'utilisateur peut modérer cette question
        can_moderate = request.user.is_authenticated and (request.user.is_staff or request.user == session.createur)
        
        # Ajouter les données de la question
        questions_data.append({
            'id': question.id,
            'contenu': question.contenu,
            'type': question.type,
            'est_anonyme': question.est_anonyme,
            'auteur_nom': question.auteur.get_full_name() if question.auteur and not question.est_anonyme else "Anonyme",
            'date_creation': timesince(question.date_creation),
            'votes_count': question.votes_count,
            'est_epinglee': question.est_epinglee,
            'est_repondue': question.est_repondue,
            'user_has_voted': user_has_voted,
            'can_moderate': can_moderate,
        })
    
    return JsonResponse({
        'questions': questions_data,
        'session': {
            'id': session.id,
            'titre': session.titre,
            'description': session.description,
            'est_active': session.est_active,
            'est_moderee': session.est_moderee,
        }
    })
