#!/bin/bash

# Grace Events Backend - Script de démarrage rapide

echo "🚀 Démarrage de Grace Events Backend..."

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer/mettre à jour les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Vérifier si le fichier .env existe
if [ ! -f ".env" ]; then
    echo "⚙️  Création du fichier .env..."
    cp env.example .env
    echo "⚠️  Veuillez configurer le fichier .env avec vos paramètres"
fi

# Appliquer les migrations
echo "🗄️  Application des migrations..."
python manage.py makemigrations
python manage.py migrate

# Créer un superutilisateur si nécessaire
echo "👤 Voulez-vous créer un superutilisateur ? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Démarrer le serveur
echo "🌐 Démarrage du serveur Django..."
echo "📍 Le serveur sera accessible sur http://127.0.0.1:8000/"
echo "🔗 API disponible sur http://127.0.0.1:8000/api/"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo ""

python manage.py runserver 