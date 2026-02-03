#!/bin/bash
cd /home/david/apps/MYAROU
git fetch --all
git reset --hard origin/main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart myarou
sudo systemctl reload nginx
