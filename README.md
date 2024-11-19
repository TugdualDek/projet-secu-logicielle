# Web Application Vulnerability Scanner

## Description

Ce projet est un scanner de vulnérabilités automatique pour applications web, développé dans le cadre du cours de sécurité logicielle. Il permet d'effectuer des tests de sécurité automatisés sur des applications web en utilisant un système de workflows personnalisables.

## Disclaimer

**Ce projet est développé à des fins éducatives uniquement.** Les auteurs ne peuvent être tenus responsables de toute utilisation malveillante ou non autorisée de cet outil.

## Architecture

#### Technologies utilisées
- **Backend**: Python avec Flask pour l'API RESTful
- **Frontend**: React.js
- **Base de données**: PostgreSQL
- **File d'attente**: Redis
- **Conteneurisation**: Docker & Docker Compose

#### Fonctionnalités principales
- Scanner automatique de vulnérabilités web
- Interface utilisateur intuitive
- Système de workflows YAML personnalisables
- Génération de rapports détaillés
- Gestion des tâches asynchrones

## Installation

### Option 1: Installation avec Docker (Recommandée)

#### Environnement de production

```bash
# Cloner le dépôt
git clone https://github.com/TugdualDek/projet-secu-logicielle.git
cd projet-secu-logicielle

# Créer et configurer le fichier .env
cp .env.example .env

# Lancer l'application en production
docker-compose -f docker-compose.prod.yml up --build
```

#### Environnement de développement

```bash
# Lancer l'application en mode développement
docker-compose -f docker-compose.dev.yml up --build
```

### Option 2: Installation manuelle

1. Prérequis
- Python 3.8+
- Node.js 18+
- PostgreSQL
- Redis
2. Installation du backend

```bash
# Installation des dépendances Python
pip3 install -r requirements.txt

# Démarrage de Redis
redis-server
```
3. Installation du frontend

```bash
cd frontend
npm run build
```

3. Configuration
- Créer un fichier .env à la racine du projet
- Configurer les variables d'environnement selon .env.example
4. Lancement

```bash
# Terminal 1 - Serveur global
python3 server.py

# Terminal 2 - Workers Redis Queue

rq worker scan_tasks --with-scheduler
```

## Architecture des workflows
Le scanner utilise un système de workflows YAML pour définir les tests de vulnérabilités. Cette approche modulaire permet d'ajouter facilement de nouveaux tests sans modifier le code source.

### Structure d'un workflow
```yaml
name: Nom du test
description: Description du test
steps:
  - module: module_name
    params:
      param1: value1
```

## Utilisation

1. Accédez à l'interface web : http://localhost:5000
2. Créez un nouveau scan
3. Lancer le scan
4. Attendez que le scan soit fini
5. Consultez les résultats du scan