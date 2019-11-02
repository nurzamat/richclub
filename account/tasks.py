from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger
from celery import task

from account.views import calculate_bonus

logger = get_task_logger(__name__)


# @periodic_task(
#    run_every=(crontab(minute='*/1')),
#    name="task_calculate_bonus",
#    ignore_result=True
# )
def task_calculate_bonus_test():
    """
    Saves latest image from Flickr
    """
    # calculate_parent_bonus()
    logger.info("Saved image from Flickr")


@task()
def task_calculate_bonus():
    logger.info("calculate bonus starts")
    calculate_bonus()


