from django.contrib.gis.db import models


class WktFile(models.Model):
    name = models.CharField(max_length=30)
    filename = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    