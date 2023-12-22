from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from core.config import SETTINGS


__all__ = ('celery_app',)


celery_app = Celery(
    'celery_app',
    broker=SETTINGS.BROKER_URI,
    backend=SETTINGS.BACKEND_URI,
)

celery_app.conf.result_expires = timedelta(hours=1)

celery_app.conf.beat_schedule = {
    'test_schedule': {
        'task': 'test_schedule',
        'schedule': crontab(minute=0, hour=15),
        'options': {
            'queue': SETTINGS.SCHEDULE_QUEUE,
        }
    }
}