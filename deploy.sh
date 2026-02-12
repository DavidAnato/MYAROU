#!/bin/bash

# -----------------------------
# Déploiement automatique MYAROU
# -----------------------------

# Variables
APP_DIR="/home/david/apps/MYAROU"
GIT_REPO="https://github.com/DavidAnato/MYAROU.git"
VENV_DIR="$APP_DIR/venv"
SERVICE_NAME="myarou"

echo "📂 Déploiement de MYAROU..."

# 1️⃣ Aller dans le dossier de l'app
cd $APP_DIR || { echo "Le dossier MYAROU n'existe pas"; exit 1; }

# 2️⃣ Initialiser git si nécessaire
if [ ! -d ".git" ]; then
    git init
    git remote add origin $GIT_REPO
fi

# 3️⃣ Récupérer le code depuis GitHub
git fetch --all
git reset --hard origin/main

# 4️⃣ Corriger les permissions critiques (Compatible Gunicorn/Nginx)
sudo chown -R david:www-data $APP_DIR
sudo chmod -R 775 $APP_DIR
chmod +x deploy.sh

# 5️⃣ Activer l'environnement virtuel
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "🔹 Aucun venv trouvé, en création..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
fi

# 6️⃣ Installer les dépendances
pip install -r requirements.txt

# 7️⃣ Créer les migrations si nécessaire et appliquer
python manage.py makemigrations
python manage.py migrate

# 7️⃣.1️⃣ Créer un superuser s'il n'existe pas
# Remplacez les valeurs ci-dessous ou utilisez des variables d'environnement
export DJANGO_SUPERUSER_PASSWORD='password_a_changer'
export DJANGO_SUPERUSER_USERNAME='admin'
export DJANGO_SUPERUSER_EMAIL='admin@example.com'

python manage.py createsuperuser --noinput || echo "Superuser existe déjà ou erreur lors de la création"

# 8️⃣ Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 9️⃣ Redémarrer le service Gunicorn
sudo systemctl restart $SERVICE_NAME

echo "✅ Déploiement terminé avec succès !"
