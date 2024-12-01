# Étape 1 : Construire l'application React
FROM node:20 AS build-react

WORKDIR /app/frontend

# Copier le fichier package.json et package-lock.json
COPY frontend/package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application React
COPY frontend/ ./

ENV NEXT_TELEMETRY_DISABLED=1

# Construire l'application React
RUN npm run build

# Étape 2 : Construire l'application Python
FROM python:3.11-slim AS finale

# Installer les outils nécessaires pour psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Créer un utilisateur non-root
RUN groupadd -r scanner && useradd -r -g scanner scanner

# Créer et configurer le répertoire de l'application
WORKDIR /app
RUN chown scanner:scanner /app

# Copier le fichier requirements.txt et installer les dépendances
COPY --chown=scanner:scanner requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu du backend avec les bonnes permissions
COPY --chown=scanner:scanner backend/ ./backend

# Copier les fichiers build de React avec les bonnes permissions
COPY --chown=scanner:scanner --from=build-react /app/frontend/build ./frontend/build

# Copier le fichier server.py
COPY --chown=scanner:scanner server.py .

# Changer vers l'utilisateur non-root
USER scanner

EXPOSE 5000