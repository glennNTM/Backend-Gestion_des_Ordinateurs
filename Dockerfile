# Dockerfile

# Étape 1 : Base image
FROM python:3.11-slim

# Étape 2 : Définir le répertoire de travail
WORKDIR /app

# Étape 3 : Copier les fichiers
COPY . /app

# Étape 4 : Installer les dépendances
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Étape 5 : Exposer le port (Render utilise le port 8000 par défaut)
EXPOSE 8000

# Étape 6 : Commande pour démarrer le serveur
CMD ["gunicorn", "gestion_ordinateurs.wsgi:application", "--bind", "0.0.0.0:8000"]
