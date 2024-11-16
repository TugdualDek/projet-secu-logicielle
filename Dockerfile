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

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy application files
COPY . .

ENV PYTHONPATH=/app