# Generated by Django 4.2.4 on 2023-12-19 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0021_ladle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ladle',
            name='time_daily',
        ),
        migrations.RemoveField(
            model_name='ladle',
            name='time_life',
        ),
    ]