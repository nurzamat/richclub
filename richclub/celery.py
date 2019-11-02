from __future__ import absolute_import

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'richclub.settings')
app = Celery('richclub')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls bonus_calculation('bonus calculation start') every 180 seconds.
    sender.add_periodic_task(180.0, bonus_calculation.s('bonus calculation start'), name='bonus calculation every 180')

    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #    crontab(hour=7, minute=30, day_of_week=1),
    #    test.s('Happy Mondays!'),
    # )


@app.task
def test(arg):
    print(arg)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(ignore_result=True)
def bonus_calculation(arg):
    print(arg)
    # from account.tasks import task_calculate_bonus
    # task_calculate_bonus()

