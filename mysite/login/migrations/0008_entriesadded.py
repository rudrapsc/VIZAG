# Generated by Django 5.0 on 2023-12-09 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_ladleupdateroomwise'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntriesAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField()),
            ],
        ),
    ]