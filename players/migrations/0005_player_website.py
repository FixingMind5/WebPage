# Generated by Django 3.0.1 on 2019-12-31 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0004_auto_20191231_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]