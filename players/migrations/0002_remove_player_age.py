# Generated by Django 3.0.1 on 2020-01-05 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='age',
        ),
    ]