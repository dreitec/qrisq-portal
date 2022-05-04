from django.contrib.gis.db import models

from django.utils.translation import ugettext_lazy as _


class GlobalConfig(models.Model):
    lookback_period = models.IntegerField()
    lookback_override = models.BooleanField(default=False)
    active_storm = models.BooleanField(default=False)
