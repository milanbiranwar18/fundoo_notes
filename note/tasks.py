from celery import shared_task
from django.core.mail import send_mail

from fundoo_notes import settings


@shared_task(bind=True)
def add_fun(self):
    return "done"


@shared_task(bind=True)
def send_mail_function(self, sub, mesg, rec_user):
    send_mail(
        subject=sub,
        message=mesg,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=rec_user,
    )
    return "Mail Sent"
