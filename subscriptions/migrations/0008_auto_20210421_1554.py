# Generated by Django 3.1.5 on 2021-04-21 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0007_merge_20210421_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment', to=settings.AUTH_USER_MODEL),
        ),
    ]
