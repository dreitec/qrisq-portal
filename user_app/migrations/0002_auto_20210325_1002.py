# Generated by Django 3.1.5 on 2021-03-25 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='street_number',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
