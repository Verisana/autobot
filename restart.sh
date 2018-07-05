systemctl restart nginx
systemctl restart uwsgi
supervisorctl restart botbtc-celery-groups:*
