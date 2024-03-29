# Generated by Django 3.1.5 on 2022-05-06 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lookback_period', models.IntegerField()),
                ('lookback_override', models.BooleanField(default=False)),
                ('active_storm', models.BooleanField(default=False)),
                ('geocode_users', models.BooleanField(default=True)),
            ],
        ),
    ]
