# Generated by Django 3.1.5 on 2021-07-02 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StormFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('folder', models.CharField(max_length=100)),
                ('filename', models.CharField(max_length=100)),
                ('etag', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]