from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import UserModel
from api.models import TimeStampedModel


# Create your models here.
class Company(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    visible = models.BooleanField(default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    guests = models.ManyToManyField(UserModel, related_name="guests")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class InviteStatuses(models.TextChoices):
    PENDING = "P", "Pending"
    CANCELED = "C", "Canceled"
    DECLINED = "D", "Declined"
    ACCEPTED = "A", "Accepted"


class Invite(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    guest = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="company_guest")
    token = models.CharField(max_length=255)
    status = models.CharField(
        max_length=1,
        choices=InviteStatuses.choices,
        default=InviteStatuses.PENDING,
    )


class RequestStatuses(models.TextChoices):
    PENDING = "P", "Pending"
    CANCELED = "C", "Canceled"
    REJECTED = "R", "Rejected"
    APPROVED = "A", "Approved"


class Request(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="company_requester")
    status = models.CharField(
        max_length=1,
        choices=RequestStatuses.choices,
        default=RequestStatuses.PENDING,
    )
