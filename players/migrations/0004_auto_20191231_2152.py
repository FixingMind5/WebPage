# Generated by Django 3.0.1 on 2019-12-31 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_auto_20191231_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.ImageField(null=True, upload_to='players/player_photos/'),
        ),
    ]
