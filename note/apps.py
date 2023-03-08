from django.apps import AppConfig


class NoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'note'

    def ready(self):
        from . import celery_redis
