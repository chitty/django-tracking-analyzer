from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django_countries.fields import CountryField

from .manager import TrackerManager


@python_2_unicode_compatible
class Tracker(models.Model):
    """
    A generic tracker model, which can be related to any other model to track
    actions that involves it.
    """
    PC = 'pc'
    MOBILE = 'mobile'
    TABLET = 'tablet'
    BOT = 'bot'
    UNKNOWN = 'unknown'
    DEVICE_TYPE = (
        (PC, 'PC'),
        (MOBILE, 'Mobile'),
        (TABLET, 'Tablet'),
        (BOT, 'Bot'),
        (UNKNOWN, 'Unknown'),
    )

    action = models.CharField(max_length=128, default='dashboard')
    action_params = models.TextField(default='')
    request_type = models.CharField(max_length=128, choices=(
        ('POST', 'POST'), ('GET', 'GET'), ('DELETE', 'DELETE'), ('UPDATE', 'UPDATE')), default='GET')
    request_source = models.CharField(max_length=128, choices=(('API', 'API'), ('UI', 'UI')), default='UI')
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    ip_country = CountryField(blank=True)
    ip_region = models.CharField(max_length=255, blank=True)
    ip_city = models.CharField(max_length=255, blank=True)
    referrer = models.URLField(blank=True)
    device_type = models.CharField(
        max_length=10, choices=DEVICE_TYPE, default=UNKNOWN)
    device = models.CharField(max_length=30, blank=True)
    browser = models.CharField(max_length=30, blank=True)
    browser_version = models.CharField(max_length=30, blank=True)
    system = models.CharField(max_length=30, blank=True)
    system_version = models.CharField(max_length=30, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, unique=False, on_delete=models.CASCADE)

    objects = TrackerManager()

    def __str__(self):
        return '{0}:{1} :: {2}, {3}'.format(
            self.request_source, self.action, self.user, self.timestamp)
