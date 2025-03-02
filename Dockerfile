# syntax=docker/dockerfile:1.4

# Utiliser une image Alpine avec Python pour une taille réduite
FROM python:3.10-alpine AS builder

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances et installer les modules Python
COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir -r requirements.txt

# Copier le code de l'application dans l'image
COPY . /app/
RUN mkdir -p /app/tmp/1234

# Commande par défaut pour exécuter l'application
ENTRYPOINT ["python3"]
CMD ["devloapp.py"]
