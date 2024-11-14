import datetime
import logging

from django.db.models import Model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Company

logger = logging.getLogger("django")


@receiver(post_save, sender=Company)
def create_company_log(sender: type[Model], instance: Model, created: bool, **kwargs: dict) -> None:
    if created:
        logger.info(f"{datetime.datetime.now()} - Company created: {instance}")
    else:
        logger.info(f"{datetime.datetime.now()} - Company updated: {instance}")


@receiver(post_delete, sender=Company)
def delete_company_log(sender: type[Model], instance: Model, **kwargs: dict) -> None:
    logger.info(f"{datetime.datetime.now()} - Company deleted: {instance}")
