# Generated by Django 2.1.7 on 2019-02-23 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20190223_1601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='pics',
        ),
    ]