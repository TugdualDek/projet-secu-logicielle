# Étape 1 : Construire l'application React
FROM node:20 AS build-react

WORKDIR /app/frontend

# Copier le fichier package.json et package-lock.json
COPY frontend/package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste de l'application React
COPY frontend/ ./

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

WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu du backend
COPY backend/ ./backend

# Copier les fichiers build de React - Correction du chemin
COPY --from=build-react /app/frontend/build ./frontend/build

COPY vulnerabilities/ ./vulnerabilities

# Copier le fichier server.py
COPY server.py .

EXPOSE 5000
