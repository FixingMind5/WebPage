# Generated by Django 3.0.5 on 2020-04-11 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField()),
                ('description', models.CharField(blank=True, max_length=140, null=True)),
                ('image', models.ImageField(default='default_user.png', null=True, upload_to='player_profile_images/')),
                ('facebook', models.CharField(blank=True, max_length=200, null=True)),
                ('twitter', models.CharField(blank=True, max_length=200, null=True)),
                ('instagram', models.CharField(blank=True, max_length=200, null=True)),
                ('youtube', models.CharField(blank=True, max_length=200, null=True)),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
                ('points', models.IntegerField(default=0, null=True)),
                ('cluster', models.CharField(default='Starter', max_length=30)),
                ('grade', models.CharField(default='Thinker', max_length=40)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]