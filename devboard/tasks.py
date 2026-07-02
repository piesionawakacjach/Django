from celery import Celery, shared_task

from devboard.models import Task

app = Celery("")

@shared_task
def send_overdue_digest():
    overdue = Task.objects.overdue()
    content = f"Zadania z przekroczonym harmonogramem: {overdue}"
    print(content)
    return overdue.count()