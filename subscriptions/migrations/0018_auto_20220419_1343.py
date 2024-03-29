# Generated by Django 3.1.5 on 2022-04-19 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0017_auto_20220110_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='user_subscription',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_payments', to='subscriptions.usersubscription'),
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=20)),
                ('discount', models.FloatField(default=0)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount', to='subscriptions.subscriptionplan')),
            ],
        ),
    ]
