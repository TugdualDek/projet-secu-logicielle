# Étape 1 : Construire l'application React
FROM node:20 AS build-react

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier package.json et package-lock.json
COPY frontend/package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application React
COPY frontend/ ./

# Construire l'application React
RUN npm run build

# Étape 2 : Construire l'application Python
FROM python:3.11-slim AS build-python

# Installer les outils nécessaires pour psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu du backend dans le conteneur
COPY backend/ ./backend

# Copier le fichier server.py de la racine
COPY server.py .

# Étape 3 : Créer l'image finale
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers construits de l'application React
COPY --from=build-react /app/build ./frontend/build

# Copier le contenu de l'application Python
COPY --from=build-python /app .

# Exposer le port 5000
EXPOSE 5000

# Définir la commande par défaut
#CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "server:app"]