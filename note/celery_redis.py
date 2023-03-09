import json
from datetime import timedelta, datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from note.models import Note


@receiver(post_save, sender=Note)
def create_reminder(sender, instance, **kwargs):
    if instance.reminder is not None:
        hrs = instance.reminder.hour
        min = instance.reminder.minute
        id = str(instance.id)
        cur_date = datetime.now()
        rem_date = instance.reminder.date()
        no_of_days = (rem_date - cur_date.date()).days
        rem_time = datetime.now() + timedelta(days=no_of_days)
        schedule, created = CrontabSchedule.objects.get_or_create(hour=hrs, minute=min, day_of_month=rem_time.day,
                                                                  month_of_year=instance.reminder.month)
        existing_task = PeriodicTask.objects.filter(name=f"Task for note {instance.id}").first()
        if existing_task is not None:
            existing_task.crontab = schedule
            existing_task.save()
        else:
            task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_" + id,
                                               task='note.tasks.send_mail_function',
                                               args=json.dumps(
                                                   [instance.title, instance.description, [instance.user.email]]))
