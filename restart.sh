systemctl restart nginx
systemctl restart uwsgi
supervisorctl restart autobot-celery-groups:*
