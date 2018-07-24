from celery import shared_task
from .models import APIKeyQiwi


@shared_tasks
def qiwi_status_updater():
    qiwis = APIKeyQiwi.objects.filter(is_blocked=False)
    for qiwi in qiwis:
        wallet =
    #check balance
    #check qiwi block
    pass

@shared_tasks
def qiwi_limit_resetter():
    qiwis = APIKeyQiwi.objects.all()
    for qiwi in qiwis:
        if qiwi.is_blocked:
            qiwi.limit_left = 0
            qiwi.save(updated_fields=['limit_left'])
        else:
            qiwi.limit_left = 50000
            qiwi.save(updated_fields=['limit_left'])

@shared_tasks
def qiwi_profit_fixator():
    pass