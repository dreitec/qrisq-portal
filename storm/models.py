from django.db import models

from core.validators import NUMERIC_VALIDATOR
from .managers import StormManager


class StormAdvisory(models.Model):
    year = models.CharField(max_length=4, validators=[NUMERIC_VALIDATOR], null=True)
    tcid = models.CharField(max_length=4, null=True)
    adv = models.CharField(max_length=2, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    direction = models.CharField(max_length=9, null=True)
    speed = models.IntegerField(null=True)
    wind = models.IntegerField(null=True)
    pressure = models.IntegerField(null=True)
    issued_datetime = models.DateTimeField(null=True)
    last_processed_datetime = models.DateTimeField(null=True)

class StormData(models.Model):
    qid = models.IntegerField()
    storm_advisory = models.ForeignKey(StormAdvisory, on_delete=models.CASCADE, related_name="advisory")
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
