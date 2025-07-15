"""
Paramètres Django spécifiques pour le déploiement sur Heroku.
Ce fichier est utilisé uniquement en production sur Heroku.
"""

from .settings import *  # Importe tous les paramètres du fichier settings.py standard

import os
import dj_database_url

# Configuration de la base de données PostgreSQL
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Activer whitenoise pour les fichiers statiques
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Désactiver le mode debug
DEBUG = False

# Sécurité supplémentaire pour la production
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
