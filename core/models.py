from django.contrib.gis.db import models


class WktFile(models.Model):
    name = models.CharField(max_length=30)
    filename = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StormFiles(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    folder = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    etag = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.folder}: {self.filename}"
