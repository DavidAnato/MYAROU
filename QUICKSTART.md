# 🚀 Guide de Démarrage Rapide

## Installation et Lancement

### Option 1 : Script automatique (Recommandé)
```bash
cd blog_project
./start.sh
```

### Option 2 : Étape par étape
```bash
cd blog_project

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Créer les données de test (optionnel)
python manage.py create_test_data

# Lancer le serveur
python manage.py runserver
```

## Accès au Projet

### URLs
- **Site web** : http://127.0.0.1:8000/
- **Interface Admin** : http://127.0.0.1:8000/admin/

### Comptes de Test
- **Admin** : `admin` / `admin123`
- **Utilisateur** : `john` / `john123`

## Fonctionnalités Principales

### 1. Interface Admin Jazzmin (Fancy)
- Design moderne et élégant
- Menu personnalisé avec icônes
- Recherche avancée
- Thème sombre/clair
- Statistiques en temps réel

**Accès** : http://127.0.0.1:8000/admin/

### 2. Éditeur HTML Riche (CKEditor)
- Formatage de texte complet
- **Upload d'images** directement dans l'éditeur
- Insertion de tableaux
- Code snippets
- Vidéos
- Liens

**Où l'utiliser** :
- Contenu des articles
- Description des catégories
- Bio des auteurs

### 3. Gestion des Articles
- Brouillon, Publié, Archivé
- Auto-génération des slugs
- SEO (meta description, keywords)
- Tags
- Statistiques de vues
- Actions en masse

### 4. Organisation
- Catégories avec images
- Auteurs avec profils complets
- Tags pour classification

## Utilisation de l'Éditeur CKEditor

### Upload d'Images dans les Articles

1. Allez dans Admin → Articles → Ajouter un article
2. Dans le champ "Contenu", cliquez sur l'icône **Image** 📷
3. Dans la fenêtre qui s'ouvre :
   - Onglet "Upload" : Cliquez sur "Choose File" et sélectionnez votre image
   - Cliquez sur "Send it to the Server"
   - L'image apparaîtra dans la galerie
4. Sélectionnez l'image et cliquez "OK"
5. L'image est maintenant dans votre article !

### Fonctionnalités de l'Éditeur

- **Formatage** : Gras, Italique, Souligné
- **Titres** : H1, H2, H3, etc.
- **Listes** : Numérotées et à puces
- **Tableaux** : Création et édition
- **Liens** : Internes et externes
- **Citations** : Blockquotes
- **Code** : Snippets de code colorés
- **Alignement** : Gauche, Centre, Droite, Justifié

## Structure du Projet

```
blog_project/
├── blog/                      # Application principale
│   ├── models.py             # Modèles (Article, Auteur, Category)
│   ├── admin.py              # Configuration admin
│   ├── views.py              # Vues
│   ├── urls.py               # URLs
│   └── management/
│       └── commands/
│           └── create_test_data.py
├── blog_project/             # Configuration
│   ├── settings.py           # Paramètres (Jazzmin, CKEditor)
│   └── urls.py               # URLs principales
├── templates/                # Templates HTML
│   ├── base.html            # Template de base
│   └── blog/                # Templates du blog
├── static/                   # CSS, JS, images statiques
│   └── css/
│       └── style.css        # CSS personnalisé
├── media/                    # Uploads utilisateurs
│   ├── articles/            # Images d'articles
│   ├── categories/          # Images de catégories
│   ├── auteurs/             # Photos d'auteurs
│   └── uploads/             # Uploads CKEditor
├── requirements.txt          # Dépendances
├── start.sh                 # Script de démarrage
└── README.md                # Documentation complète
```

## Créer du Contenu

### 1. Créer une Catégorie
1. Admin → Catégories → Ajouter
2. Remplir le nom (le slug se génère auto)
3. Ajouter une description avec l'éditeur HTML
4. (Optionnel) Ajouter une image
5. Enregistrer

### 2. Créer un Auteur
1. Admin → Auteurs → Ajouter
2. Sélectionner un utilisateur
3. Ajouter une bio (avec HTML riche)
4. (Optionnel) Photo, site web, Twitter
5. Enregistrer

### 3. Créer un Article
1. Admin → Articles → Ajouter
2. **Titre** : Saisissez le titre
3. **Auteur** : Choisissez l'auteur
4. **Catégorie** : Choisissez la catégorie
5. **Contenu** : Utilisez l'éditeur pour :
   - Écrire votre texte
   - Ajouter des images (via le bouton Image)
   - Formater le contenu
6. **Extrait** : Court résumé (optionnel)
7. **Image** : Image principale de l'article
8. **Tags** : Séparés par des virgules
9. **Statut** : 
   - Brouillon (pas visible)
   - Publié (visible sur le site)
   - Archivé
10. **SEO** : Meta description et keywords
11. Enregistrer

## Actions en Masse

Depuis la liste des articles :
1. Cochez plusieurs articles
2. Dans "Action", choisissez :
   - "Publier les articles sélectionnés"
   - "Mettre en brouillon"
3. Cliquez "Aller"

## Personnalisation

### Modifier le Thème Jazzmin
Éditez `blog_project/settings.py` :
- `JAZZMIN_SETTINGS` : Configuration générale
- `JAZZMIN_UI_TWEAKS` : Couleurs et apparence

### Modifier les Templates
Les templates sont dans `templates/blog/` :
- `article_list.html` : Page d'accueil
- `article_detail.html` : Détail d'un article
- `category_detail.html` : Articles par catégorie
- `auteur_detail.html` : Articles par auteur

### CSS Personnalisé
Fichier : `static/css/style.css`

## Commandes Utiles

```bash
# Créer des données de test
python manage.py create_test_data

# Créer un super utilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Shell Django
python manage.py shell
```

## Résolution de Problèmes

### Les images ne s'affichent pas
1. Vérifiez que `MEDIA_URL` et `MEDIA_ROOT` sont configurés dans `settings.py`
2. Vérifiez que les URLs incluent les fichiers media en mode DEBUG

### L'éditeur CKEditor ne fonctionne pas
1. Vérifiez que `ckeditor` et `ckeditor_uploader` sont dans `INSTALLED_APPS`
2. Vérifiez que les URLs de CKEditor sont configurées

### Erreur lors de l'upload
1. Vérifiez que Pillow est installé : `pip install Pillow`
2. Vérifiez les permissions du dossier `media/`

## Technologies

- **Django 5.2.8** : Framework web
- **Bootstrap 5** : Framework CSS
- **CKEditor** : Éditeur HTML riche avec upload d'images
- **Jazzmin 3.0.1** : Interface admin moderne
- **Font Awesome** : Icônes
- **Pillow** : Traitement d'images

## Support

Pour toute question :
1. Consultez `README.md` pour plus de détails
2. Vérifiez la documentation Django : https://docs.djangoproject.com/
3. Documentation CKEditor : https://ckeditor.com/docs/

---

**Bon blogging ! 🎉**
