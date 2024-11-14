from django.contrib.auth import get_user_model
from django.db import models

from api.models import TimeStampedModel


# Create your models here.
class Company(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    visible = models.BooleanField(default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
