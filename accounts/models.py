from django.db import models
from django.contrib.auth.models import AbstractUser

from api.models import TimeStampedModel


# Create your models here.
class UserModel(TimeStampedModel, AbstractUser):
    image_path = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self) -> str:
        return self.username
