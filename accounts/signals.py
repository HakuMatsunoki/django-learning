import datetime
import logging

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

logger = logging.getLogger("django")


@receiver(post_save, sender=get_user_model())
def create_user_log(sender: type[Model], instance: Model, created: bool, **kwargs: dict) -> None:
    if created:
        logger.info(f"{datetime.datetime.now()} - User created: {instance}")
    else:
        logger.info(f"{datetime.datetime.now()} - User updated: {instance}")


@receiver(post_delete, sender=get_user_model())
def delete_user_log(sender: type[Model], instance: Model, **kwargs: dict) -> None:
    logger.info(f"{datetime.datetime.now()} - User deleted: {instance}")
