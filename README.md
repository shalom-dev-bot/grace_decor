# Grace Events - Backend API

Backend Django REST API pour la plateforme de gestion d'événements Grace Events.

## 🚀 Technologies

- **Django 5.2.5** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données
- **JWT Authentication** - Authentification par tokens
- **Django CORS Headers** - Gestion CORS
- **Pillow** - Traitement d'images
- **Python Decouple** - Gestion des variables d'environnement

## 📋 Prérequis

- Python 3.8+
- PostgreSQL
- pip

## 🛠️ Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd glow
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données PostgreSQL**
```sql
CREATE DATABASE grace;
CREATE USER grace_user WITH PASSWORD 'grace123';
GRANT ALL PRIVILEGES ON DATABASE grace TO grace_user;
```

5. **Configurer les variables d'environnement**
Créer un fichier `.env` à la racine du projet :
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://grace_user:grace123@localhost:5432/grace
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

6. **Appliquer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

8. **Lancer le serveur**
```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://127.0.0.1:8000/`

## 📁 Structure du Projet

```
glow/
├── glow_backend/          # Configuration principale Django
│   ├── settings.py       # Paramètres du projet
│   ├── urls.py          # URLs principales
│   └── wsgi.py          # Configuration WSGI
├── core/                 # Application utilisateurs
├── events/              # Application événements
├── bookings/            # Application réservations
├── payments/            # Application paiements
├── testimonials/        # Application témoignages
├── packages/            # Application packages
├── services/            # Application services
├── announcements/       # Application annonces
├── staff/               # Application personnel
├── media_app/           # Application médias
├── requirements.txt     # Dépendances Python
└── manage.py           # Script de gestion Django
```

## 🔐 API Endpoints

### Authentification
- `POST /api/core/register/` - Inscription utilisateur
- `POST /api/core/login/` - Connexion utilisateur
- `GET /api/core/activate/<token>/` - Activation compte
- `PATCH /api/core/profile/update/` - Mise à jour profil
- `PATCH /api/core/profile/upload-image/` - Upload image profil

### Événements
- `GET /api/events/events/` - Liste des événements
- `POST /api/events/events/` - Créer un événement
- `GET /api/events/events/<id>/` - Détails événement
- `PUT /api/events/events/<id>/` - Modifier événement
- `DELETE /api/events/events/<id>/` - Supprimer événement

### Réservations
- `GET /api/bookings/bookings/` - Liste des réservations
- `POST /api/bookings/bookings/` - Créer une réservation
- `GET /api/bookings/bookings/<id>/` - Détails réservation

### Paiements
- `GET /api/payments/payments/` - Liste des paiements
- `POST /api/payments/payments/` - Créer un paiement
- `GET /api/payments/payments/<id>/` - Détails paiement
- `POST /api/payments/payments/<id>/process/` - Traiter paiement

### Témoignages
- `GET /api/testimonials/testimonials/public/` - Témoignages publics
- `GET /api/testimonials/testimonials/featured/` - Témoignages mis en avant
- `POST /api/testimonials/testimonials/` - Créer un témoignage
- `POST /api/testimonials/testimonials/<id>/approve/` - Approuver témoignage
- `POST /api/testimonials/testimonials/<id>/reject/` - Rejeter témoignage

### Packages
- `GET /api/packages/packages/` - Liste des packages
- `POST /api/packages/packages/` - Créer un package

### Services
- `GET /api/services/services/` - Liste des services
- `POST /api/services/services/` - Créer un service

### Annonces
- `GET /api/announcements/announcements/` - Liste des annonces
- `POST /api/announcements/announcements/` - Créer une annonce

## 🔧 Configuration

### Variables d'environnement

Créer un fichier `.env` avec les variables suivantes :

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://grace_user:grace123@localhost:5432/grace

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

### Base de données

Le projet utilise PostgreSQL. Assurez-vous d'avoir :

1. PostgreSQL installé et en cours d'exécution
2. Une base de données `grace` créée
3. Un utilisateur `grace_user` avec les permissions appropriées

## 🚀 Déploiement

### Production

1. **Configurer les variables d'environnement de production**
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:password@host:port/database
```

2. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic
```

3. **Configurer un serveur web (nginx, apache)**
4. **Configurer un serveur WSGI (gunicorn, uwsgi)**

### Docker (optionnel)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "glow_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 📝 Modèles de données

### Utilisateur (CustomUser)
- Informations de base (nom, email, téléphone)
- Rôle (client, admin, agency)
- Profil (bio, adresse, langue)
- Image de profil
- Statut de vérification

### Événement
- Titre, description, date, lieu
- Type d'événement (classic, modern, vip)
- Images
- Package associé
- Statut

### Réservation
- Événement associé
- Client
- Date de réservation
- Montant payé
- Statut

### Paiement
- Réservation associée
- Montant, devise
- Méthode de paiement
- Statut de transaction
- Informations de facturation

### Témoignage
- Client
- Titre, contenu, note
- Type d'événement, date, lieu
- Statut (en attente, approuvé, rejeté)
- Mis en avant

## 🔐 Sécurité

- **JWT Authentication** pour l'API
- **CORS** configuré pour le frontend
- **Validation** des données côté serveur
- **Permissions** basées sur les rôles
- **Variables d'environnement** pour les secrets

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Tests d'une application spécifique
python manage.py test core
python manage.py test events
```

## 📊 Monitoring

- **Logs** Django configurés
- **Statistiques** des paiements
- **Métriques** des événements
- **Rapports** des témoignages

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📞 Support

Pour toute question ou problème :
- Ouvrir une issue sur GitHub
- Contacter l'équipe de développement

---

**Grace Events** - Plateforme de gestion d'événements moderne et intuitive. 