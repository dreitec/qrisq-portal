from django.db import models
from user_app.models import User


class PaypalCapture(models.Model):
    capture_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="capture")
