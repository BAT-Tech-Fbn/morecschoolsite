from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('evenements/', views.evenements, name='evenements'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('register/', views.register, name='register'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('ajouter-evenement/', views.ajouter_evenement, name='ajouter_evenement'),
    path('gestion-evenements/', views.gestion_evenements, name='gestion_evenements'),
    path('enregistrer-caroussel-image/', views.enregistrer_caroussel_image, name='enregistrer_caroussel_image'),
    path('reglage/', views.reglage, name='reglage'),
    path('gestion-utilisateurs/', views.gestion_utilisateurs, name='gestion_utilisateurs'),
    path('enregistrer-video/', views.enregistrer_video, name='enregistrer_video'),
    path('gestion-temoignages/', views.gestion_temoignages, name='gestion_temoignages'),
    path('modifier-video/<int:video_id>/', views.modifier_video, name='modifier_video'),
    path('supprimer-video/<int:video_id>/', views.supprimer_video, name='supprimer_video'),
    path('supprimer-caroussel-image/<int:image_id>/', views.supprimer_caroussel_image, name='supprimer_caroussel_image'),
    path('modifier-caroussel-image/<int:image_id>/', views.modifier_caroussel_image, name='modifier_caroussel_image'),
    path('modifier-evenement/<int:event_id>/', views.modifier_evenement, name='modifier_evenement'),
    path('supprimer-evenement/<int:event_id>/', views.supprimer_evenement, name='supprimer_evenement'),
    path('membres/', views.membres, name='membres'),
    path('cours/', views.cours_list, name='cours_list'),
    path('masterclass-publique/', views.masterclasses_publiques, name='masterclass_publique'),
    
    # URLs pour la fonctionnalité Slido
    path('interactive/', views.accueil_interactive, name='accueil_interactive'),
    path('interactive/creer/', views.creer_session, name='creer_session'),
    path('interactive/session/<slug:session_slug>/', views.session_interactive, name='session_interactive'),
    path('interactive/session/<slug:session_slug>/questions-json/', views.session_questions_json, name='session_questions_json'),
    path('interactive/gestion/<slug:session_slug>/', views.gestion_session, name='gestion_session'),
    path('interactive/question/<int:question_id>/approuver/', views.approuver_question, name='approuver_question'),
    path('interactive/question/<int:question_id>/rejeter/', views.rejeter_question, name='rejeter_question'),
    path('interactive/question/<int:question_id>/voter/', views.voter_question, name='voter_question'),
    path('interactive/question/<int:question_id>/epingler/', views.epingler_question, name='epingler_question'),
    path('interactive/question/<int:question_id>/marquer-repondue/', views.marquer_repondue, name='marquer_repondue'),
    
    # URLs pour la gestion des MasterClasses
    path('masterclasses/', views.liste_masterclasses, name='liste_masterclasses'),
    path('masterclasses/<int:masterclass_id>/', views.detail_masterclass, name='detail_masterclass'),
    path('masterclasses/ajouter/', views.ajouter_masterclass, name='ajouter_masterclass'),
    path('masterclasses/<int:masterclass_id>/modifier/', views.modifier_masterclass, name='modifier_masterclass'),
    path('masterclasses/<int:masterclass_id>/supprimer/', views.supprimer_masterclass, name='supprimer_masterclass'),
    
    # URLs pour la gestion des Animateurs
    path('animateurs/', views.liste_animateurs, name='liste_animateurs'),
    path('animateurs/ajouter/', views.ajouter_animateur, name='ajouter_animateur'),
    path('animateurs/<int:animateur_id>/', views.detail_animateur, name='detail_animateur'),
    path('animateurs/<int:animateur_id>/modifier/', views.modifier_animateur, name='modifier_animateur'),
    path('animateurs/<int:animateur_id>/supprimer/', views.supprimer_animateur, name='supprimer_animateur'),
]
