# 1. Image de base
FROM python:3.12-slim

# Variables d'environnement Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/app/data/incidents.db

# 2. Répertoire de travail
WORKDIR /app

# 3. Installer les dépendances (copiées en premier pour profiter du cache Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copier le code de l'application
COPY app/ ./app/
COPY run.py .

# Dossier de la base SQLite
RUN mkdir -p /app/data

# 5. Exposer le port
EXPOSE 5000

# 6. Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]
