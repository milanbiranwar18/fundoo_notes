from celery import shared_task
from django.core.mail import send_mail

from fundoo_notes import settings
from user.models import User
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def add_fun(self):
    print("hello")
    return "done"


@shared_task(bind=True)
def send_mail_function(self):
    # users = User.objects.all()
    users = User.objects.filter(email='milanbiranwar18@gmail.com')
    # for user in users:
    send_mail(
        subject='sending test mail',
        message='testing by sending mail to users which we have in our database',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=users,

    )
    return "Mail Sent"
















# @shared_task(bind=True)
# def send_mail_func(self, subject, message, recipient_list):
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=recipient_list,
#         fail_silently=False,)
#     return "done"
