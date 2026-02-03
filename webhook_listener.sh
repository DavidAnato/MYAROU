#!/bin/bash

# Log des requêtes pour debug
LOGFILE="/home/david/apps/MYAROU/webhook.log"

read payload
echo "$(date) - Payload reçu : $payload" >> $LOGFILE

# Vérifie si le push est sur main
if echo "$payload" | grep -q '"ref": "refs/heads/main"'; then
    echo "$(date) - Push sur main détecté, déploiement..." >> $LOGFILE
    /home/david/apps/MYAROU/deploy.sh >> $LOGFILE 2>&1
fi
