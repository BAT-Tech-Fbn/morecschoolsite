# MorecSchool

Application web de gestion pour l'école MorecSchool, développée avec Django 5.0 et Python 3.13.

## Fonctionnalités

- Gestion des événements
- Gestion des membres
- Sessions interactives
- Système de questions anonymes
- Système de masterclass
- Paramètres administratifs

## Prérequis

- Python 3.13
- Django 5.0
- Autres dépendances listées dans requirements.txt

## Installation

1. Clonez ce dépôt
2. Créez un environnement virtuel : `python -m venv venv`
3. Activez l'environnement virtuel :
   - Windows : `venv\Scripts\activate` ou `.\venv\Scripts\Activate.ps1`
   - Note : En cas de problème avec l'activation, utilisez directement le chemin complet : `.\venv\Scripts\python.exe`
4. Installez les dépendances : `pip install -r requirements.txt`
5. Effectuez les migrations : `python manage.py migrate`
6. Lancez le serveur : `python manage.py runserver`

## Déploiement

Ce projet est configuré pour être déployé sur diverses plateformes comme Heroku, PythonAnywhere, ou Render.
