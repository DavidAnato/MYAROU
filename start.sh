#!/bin/bash

echo "🚀 Démarrage du projet Blog Django..."
echo ""

# Vérifier si les dépendances sont installées
if ! python -c "import django" 2>/dev/null; then
    echo "📦 Installation des dépendances..."
    pip install -r requirements.txt --break-system-packages -q
    echo "✅ Dépendances installées"
fi

# Créer les dossiers media si nécessaire
mkdir -p media/articles media/categories media/auteurs media/uploads

# Appliquer les migrations si nécessaire
echo ""
echo "🗄️  Vérification de la base de données..."
python manage.py migrate --noinput

# Collecter les fichiers statiques
echo ""
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear 2>/dev/null

echo ""
echo "✅ Projet prêt !"
echo ""
echo "📋 Informations de connexion :"
echo "   Admin: admin / admin123"
echo "   John:  john / john123"
echo ""
echo "🌐 URLs disponibles :"
echo "   Site web : http://127.0.0.1:8000/"
echo "   Admin    : http://127.0.0.1:8000/admin/"
echo ""
echo "▶️  Démarrage du serveur de développement..."
echo ""

python manage.py runserver 0.0.0.0:8000
