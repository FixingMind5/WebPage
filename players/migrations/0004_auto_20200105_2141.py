# Generated by Django 3.0.1 on 2020-01-05 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0003_remove_player_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.ImageField(default='static/images/default_user.png', null=True, upload_to='player_profile_images/'),
        ),
    ]
