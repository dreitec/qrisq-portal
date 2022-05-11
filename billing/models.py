from django.contrib.gis.db import models

from django.utils.translation import ugettext_lazy as _


class Billing(models.Model):
    TYPE = [("C", "city"), ("S", "state"), ("P", "country/parish")]
    STATUS = [
        (0, "pending"),
        (1, "active"),
        (-1, "expired"),
    ]
    type = models.CharField(max_length=1, choices=TYPE)
    name = models.CharField(max_length=60, default=None, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=None, null=True)
    discount = models.FloatField(default=0)
    users = models.IntegerField(default=0)
    shape_file = models.CharField(max_length=999, default=None, null=True)
