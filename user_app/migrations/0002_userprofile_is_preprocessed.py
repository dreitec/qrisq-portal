# Generated by Django 3.1.5 on 2021-03-24 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_preprocessed',
            field=models.BooleanField(default=False),
        ),
    ]