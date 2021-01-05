# Create your tasks here
from django.core.mail import send_mail
from celery import shared_task, Celery
import time


@shared_task
def mail_to_admin(mail):
    send_mail(
        'New creature',
        'New creature was added to DB',
        'djangotestmail@ya.ru',
        [mail],
    )
    print('Mail sent')


@shared_task
def creatures_counter():
    from .models import Creature
    c = 0
    for _ in Creature.objects.all():
        c += 1
    print(f"At {time.ctime()} in DB are {c} creatures")
