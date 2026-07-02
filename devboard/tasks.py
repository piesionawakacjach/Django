from celery import shared_task

from devboard.models import Task


@shared_task
def send_overdue_digest():
    overdue = Task.objects.is_overdue()
    content = f"Zadania z przekroczonym harmonogramem: {overdue}"
    print(content)
    return overdue.count()