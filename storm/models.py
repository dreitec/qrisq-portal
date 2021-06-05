from django.db import models

from core.validators import NUMERIC_VALIDATOR
from .managers import StormManager


class StormData(models.Model):
    qid = models.IntegerField()
    year = models.CharField(max_length=4, validators=[NUMERIC_VALIDATOR], null=True)
    adv = models.CharField(max_length=255, null=True)
    tcid = models.CharField(max_length=255, null=True)
    riskthreat = models.CharField(max_length=255, null=True)
    maxflood = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    maxwind = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    accumrain = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    windrisk = models.CharField(max_length=255, null=True)
    maxwind_dir = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    maxwind_dirname = models.CharField(max_length=255, null=True)
    landfall_location = models.CharField(max_length=255, null=True)
    landfall_datetime = models.DateTimeField(null=True)
    storm_distance = models.DecimalField(max_digits=10, decimal_places=5, null=True)
    maxflood_datetime = models.DateTimeField(null=True)
    maxwind_datetime = models.DateTimeField(null=True)
    landfall_datetime_local_string = models.CharField(max_length=255, null=True)
    maxflood_datetime_local_string = models.CharField(max_length=255, null=True)
    maxwind_datetime_local_string = models.CharField(max_length=255, null=True)

    objects = StormManager()

    class Meta:
        managed = False
        db_table = 'addressstormdata'
