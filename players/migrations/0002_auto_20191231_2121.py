# Generated by Django 3.0.1 on 2019-12-31 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='points',
            field=models.IntegerField(default=0, null=True),
        ),
    ]