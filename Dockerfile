# Base image
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exposer le port de l'app
EXPOSE 8000

# Commande à lancer
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
