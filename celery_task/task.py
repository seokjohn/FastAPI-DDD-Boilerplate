
from celery_task import celery_app
from core.config import SETTINGS
from app.user.tasks.user import test_schedule


@celery_app.task(queue=SETTINGS.SCHEDULE_QUEUE, name='test_schedule')
def user_test_schedule():
    test_schedule()

