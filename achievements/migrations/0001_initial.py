# Generated by Django 3.0.1 on 2020-02-19 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='No Title', max_length=40)),
                ('points', models.IntegerField()),
                ('description', models.CharField(default='No Description', max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='achievements/images')),
                ('type', models.CharField(max_length=10)),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='players.Player')),
            ],
        ),
    ]
