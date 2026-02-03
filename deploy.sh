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

# 4️⃣ Activer l'environnement virtuel
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
else
    echo "🔹 Aucun venv trouvé, en création..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
fi

# 5️⃣ Installer les dépendances
pip install -r requirements.txt

# 6️⃣ Appliquer les migrations Django
python manage.py makemigrations
python manage.py migrate

# 7️⃣ Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 8️⃣ Redémarrer le service systemd
sudo systemctl restart $SERVICE_NAME
sudo systemctl status $SERVICE_NAME --no-pager

# 9️⃣ Recharger Nginx
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Déploiement terminé !"
