# Generated by Django 3.1.5 on 2021-04-28 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0009_paymentrefund'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentrefund',
            name='refund_transaction_id',
        ),
    ]