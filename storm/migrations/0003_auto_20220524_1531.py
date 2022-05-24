# Generated by Django 3.1.5 on 2022-05-24 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storm', '0002_remove_stormadvisory_storm_advisory_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='stormadvisory',
            name='direction',
            field=models.CharField(max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='stormadvisory',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stormadvisory',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='stormadvisory',
            name='pressure',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='stormadvisory',
            name='speed',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='stormadvisory',
            name='wind',
            field=models.IntegerField(null=True),
        ),
    ]
