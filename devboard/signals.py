# from django.dispatch import receiver
# from django.db.models.signals import post_save
#
# def save_done_info(sender, instance,**kwargs):
#     print(f"Zapisano {instance} do bazy danych")
#
# @receiver(post_save, sender=Task, dispatch_uid="save_done_info2_on_task")
# def save_done_info2(sender, instance, **kwargs):
#     print(f"Zapisano {instance} do bazy danych (z dekoratora)")

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from devboard.models import Task

from devboard.tasks import send_overdue_digest

def save_done_info(sender, instance, **kwargs):
    print(f"Zapisano {instance} do bazy!")

@receiver(post_save, sender=Task, dispatch_uid="save_done_info2_on_taks")
def save_done_info2(sender, instance, **kwargs):
    print(f"Zapisano {instance} do bazy!")
    send_overdue_digest.delay()

@receiver(pre_save, sender=Task, dispatch_uid="task_status_change_check")
def check_old_status(sender, instance, **kwargs):
    if instance.pk:
        status = sender.objects.filter(pk=instance.pk).first().status
        print("OLD STATUS:", status)

@receiver(post_save, sender=Task, dispatch_uid="task_status_change_log")
def log_state_change(sender, instance, created, **kwargs):
    if created:
        return
    print("NEW STATUS:", instance.status)