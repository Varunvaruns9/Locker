# Generated by Django 2.1.7 on 2019-02-17 08:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Locker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_status', models.BooleanField(default=False)),
                ('accessible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('pics', models.URLField(max_length=512)),
                ('locker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Locker')),
            ],
        ),
    ]
