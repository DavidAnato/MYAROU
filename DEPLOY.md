# README – Déploiement & Mise à Jour de MYAROU

Ce document explique **le processus réel de mise à jour du projet déjà déployé en production**.

---

# 1. Connexion au serveur

```bash
ssh root@31.97.178.212

```

Entrer le mot de passe serveur lorsque demandé.

---

# 2. Aller dans le dossier du projet

```bash
cd /home/david/apps/MYAROU
```

---

# 3. Lancer la mise à jour automatique

```bash
./deploy.sh
```

Ce script fait automatiquement :

- récupération du code depuis GitHub
- installation des dépendances
- migrations Django
- collectstatic
- redémarrage de Gunicorn
- rechargement de Nginx

---

# 4. Si une erreur apparaît

## 4.1 Internal Server Error

Vérifier les logs Gunicorn :

```bash
journalctl -u myarou -n 50 --no-pager
```

Corriger l’erreur indiquée puis relancer :

```bash
./deploy.sh
```

---

## 4.2 Erreur "readonly database"

Corriger les permissions SQLite :

```bash
chown -R david:www-data /home/david/apps/MYAROU
chmod -R 775 /home/david/apps/MYAROU
```

Puis relancer :

```bash
./deploy.sh
```

---

## 4.3 Erreur 502 Bad Gateway

Redémarrer Gunicorn :

```bash
systemctl restart myarou
```

Vérifier son état :

```bash
systemctl status myarou
```

---

## 4.4 Problème de fichiers statiques

```bash
source venv/bin/activate
python manage.py collectstatic --noinput
systemctl restart myarou
```

---

# 5. Processus standard de mise à jour

À chaque modification du code :

1. **Push sur GitHub (branche main)**
2. **Connexion au serveur**
3. **Exécution de `deploy.sh`**
4. **Correction d’erreur si nécessaire**
5. **Relance de `deploy.sh`**

---

# 6. Résumé rapide

```bash
ssh root@31.97.178.212
cd /home/david/apps/MYAROU
./deploy.sh
```

Si erreur → corriger → relancer `./deploy.sh`.

---

**Projet : MYAROU**  
Déploiement Django + Gunicorn + Nginx en production.

