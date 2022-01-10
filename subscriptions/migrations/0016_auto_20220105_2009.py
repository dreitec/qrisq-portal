# Generated by Django 3.1.5 on 2022-01-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0015_userpayment_payment_id_length'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='fluidpay_plan_id',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='subscriptionplan',
            name='paypal_plan_id',
            field=models.CharField(default='', max_length=60),
        ),
        migrations.AlterField(
            model_name='userpayment',
            name='payment_id',
            field=models.CharField(default=None, max_length=60, null=True),
        ),
    ]
