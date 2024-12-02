import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.enums import UserTypeChoices, SubscriptionChoices, AdTypeChoices


class User(AbstractUser):
    email = models.EmailField(unique=True)
    user_type = models.IntegerField(choices=UserTypeChoices.choices,
                                    default=UserTypeChoices.INDIVIDUAL)
    organisation = models.ForeignKey(
        "Organization", on_delete=models.CASCADE, related_name='organization_users',
        blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription = models.IntegerField(choices=SubscriptionChoices.choices,
                                       default=SubscriptionChoices.FREE)

    def __str__(self):
        return self.username


class Organization(models.Model):
    uuid = models.UUIDField(unique=True, null=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class AdSection(models.Model):
    ad_name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    ad_type = models.CharField(
        max_length=50, choices=AdTypeChoices.choices)
    publisher = models.CharField(max_length=100)

    def __str__(self):
        return self.ad_name


class UserFeedback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    organisation = models.CharField(max_length=200, blank=True)
    feedback = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} on {self.created_at}"
