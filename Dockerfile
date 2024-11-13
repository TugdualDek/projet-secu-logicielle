# Utiliser une image Python officielle comme image parent
FROM python:3.11-slim

# Installer l'outil necessaire pour psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le contenu de votre projet dans le conteneur
COPY . .

# Exposer le port 5000
EXPOSE 5000

# Définir la commande par défaut
CMD ["flask", "run", "--host=0.0.0.0"]

# Possible d'utiliser un builder pour faire une image plus propre à la fin sans le lipqdev et gcc pour que ce soit plus leger