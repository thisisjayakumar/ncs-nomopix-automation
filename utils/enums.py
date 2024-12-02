from django.db import models
from django.utils.translation import gettext_lazy as _


class UserTypeChoices(models.IntegerChoices):
    INDIVIDUAL = 1, _("INDIVIDUAL")
    ORGANIZATION = 2, _("ORGANIZATION")
    ADMIN = 3, _("ADMIN")


class SubscriptionChoices(models.IntegerChoices):
    FREE = 1, _("FREE")
    GOLD = 2, _("GOLD")
    DIAMOND = 3, _("DIAMOND")


class AdTypeChoices(models.TextChoices):
    HEADER_ADS = 'header_ads', _("Header Ads")
    VERTICAL_SIDE_ADS = 'vertical_side_ads', _('Vertical Side Ads')
    FOOTER_ADS = 'footer_ads', _("Footer Ads")
    INTERSTITIAL_ADS = 'interstitial_ads', _("Interstitial Ads")
    VIDEO_ADS = 'video_ads', _("Video Ads")
