import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.enums import UserTypeChoices, SubscriptionChoices, AdTypeChoices


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=50, choices=UserTypeChoices.choices,
        default=UserTypeChoices.INDIVIDUAL)
    organisation = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name='organization_user',
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription = models.CharField(
        max_length=50, choices=SubscriptionChoices.choices,
        default=SubscriptionChoices.FREE)

    def __str__(self):
        return self.username


class Organization(models.Model):
    uuid = models.UUIDField(unique=True, null=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30)


class AdSection(models.Model):
    ad_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    ad_type = models.CharField(
        max_length=50, choices=AdTypeChoices.choices)
    publisher = models.CharField(max_length=100)
