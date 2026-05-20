# Déploiement MYAROU

Le site tourne sur un **VPS** (Django + Gunicorn + Nginx). Le code est sur GitHub : `DavidAnato/MYAROU`.

---

## Avant chaque déploiement (sur votre PC)

### 1. Vérifier que tout fonctionne en local

```powershell
cd "C:\Users\David Anato\Documents\Work offline\blog_project"
.\venv\Scripts\activate   # si vous utilisez un venv
pip install -r requirements.txt
python manage.py migrate
python manage.py check
```

### 2. Commiter et pousser sur `main`

Le serveur fait `git pull` via `deploy.sh` — **sans push, le serveur ne reçoit rien**.

```powershell
git add blog/ blog_project/ dashboard/ homepage/ templates/ i18n/ GALERIE.md
git status
git commit -m "feat: pages éditables, galerie, contact et liens"
git push origin main
```

Ne pas ajouter par erreur : `password`, `rapport-brief-*.pdf`, `__pycache__/`, `db.sqlite3`, `.env`.

### 3. Déploiement automatique (optionnel)

Si le **webhook GitHub** est configuré, un push sur `main` déclenche `webhook_listener.sh` → `deploy.sh` sans SSH manuel.

---

## Mise à jour sur le serveur (méthode habituelle)

### 1. Connexion SSH

```bash
ssh root@31.97.178.212
```

### 2. Lancer le script

```bash
cd /home/david/apps/MYAROU
./deploy.sh
```

Le script :

- récupère `origin/main`
- installe les dépendances (`pip install -r requirements.txt`)
- applique les migrations (`migrate`)
- collecte les statiques (`collectstatic`)
- redémarre Gunicorn (`systemctl restart myarou`)

### 3. Vérifier le site

- Page d’accueil : `/`
- Galerie : `/galerie/`
- Dashboard : `/dashboard/`

---

## Résumé une ligne

```bash
ssh root@31.97.178.212 "cd /home/david/apps/MYAROU && ./deploy.sh"
```

(À lancer **après** `git push` depuis votre PC.)

---

## Migrations récentes (galerie, contact, etc.)

Cette version ajoute notamment :

- `homepage/migrations/0003_...` (pages site, contact, galerie dédiée)
- `homepage/migrations/0004_aboutgalleryimage.py` (galerie À propos)

Elles doivent être **dans le dépôt Git** avant le déploiement. `deploy.sh` exécute uniquement `migrate`, pas `makemigrations`.

---

## En cas d’erreur

### Internal Server Error (500)

```bash
journalctl -u myarou -n 80 --no-pager
```

Souvent : migration non appliquée, module manquant, ou erreur PostgreSQL.

```bash
cd /home/david/apps/MYAROU
source venv/bin/activate
python manage.py migrate --noinput
sudo systemctl restart myarou
```

### 502 Bad Gateway

```bash
sudo systemctl status myarou
sudo systemctl restart myarou
sudo systemctl restart nginx
```

### Fichiers statiques / CSS

```bash
cd /home/david/apps/MYAROU
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart myarou
```

### Permissions (media, base de données)

```bash
sudo chown -R david:www-data /home/david/apps/MYAROU
sudo chmod -R 775 /home/david/apps/MYAROU
```

### PostgreSQL

Le serveur utilise PostgreSQL (`myarou_db`). Vérifier que le service tourne :

```bash
sudo systemctl status postgresql
```

---

## Variables d’environnement (e-mail contact)

Sur le serveur, dans le service systemd Gunicorn ou un fichier `.env` :

| Variable | Exemple |
|----------|---------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `DEFAULT_FROM_EMAIL` | `noreply@myarou.com` |
| Paramètres SMTP Django | `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` |

Sans configuration, les messages contact sont enregistrés en base mais l’e-mail part en console (logs).

---

## Alternative : Render.com

Le fichier `render.yaml` permet un déploiement sur Render (build + Gunicorn). Il faut y configurer une base PostgreSQL et les variables d’environnement (`DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`). Le VPS actuel reste la méthode principale documentée ci-dessus.

---

**Projet : MYAROU** — Django 5.2 + Gunicorn + Nginx + PostgreSQL.
