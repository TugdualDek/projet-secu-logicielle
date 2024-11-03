# FortiCheck

Application de test de sécurité web avec interface graphique nommé pour l'instant FortiCheck :)

## Prérequis

- Python 3.8+
- Node.js 14+
- MongoDB

## Installation

### 1. Backend (Python)

```bash
# Cloner le repository
git clone <votre-repo-url>
cd FortiCheck

# Créer et activer un environnement virtuel ! 
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances Python
pip install -r requirements.txt
```

### 2. Frontend (React)

```bash
# Aller dans le dossier frontend
cd frontend

# Installer les dépendances Node.js
npm install
```

### 3. Base de données

Assurez-vous que MongoDB est installé et en cours d'exécution sur le port par défaut (27017)

## Lancement de l'application

1. Lancer le backend (dans un terminal) :
```bash
python app_fortiCheck.py
# Le serveur démarre sur http://localhost:5000
```

2. Lancer le frontend (dans un autre terminal) :
```bash
cd frontend
npm start
# L'application React démarre sur http://localhost:3000
```

## Configuration

Par défaut, l'application utilise :
- Backend : http://localhost:5000
- Frontend : http://localhost:3000
- MongoDB : mongodb://localhost:27017/FortiCheck_DB

## Structure du projet

- `/attack_modules/` : Modules de test de sécurité
- `/frontend/` : Interface utilisateur React
- `/backend/` : API Flask
- `/config/` : Fichiers de configuration

## Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## .gitignore

Un fichier .gitignore est fourni pour exclure :
- Les dépendances (`node_modules`, `venv`)
- Les fichiers compilés (`__pycache__`)
- Les fichiers de configuration locaux