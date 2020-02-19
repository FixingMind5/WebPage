# Generated by Django 3.0.1 on 2020-02-19 03:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='No Title', max_length=70, null=True)),
                ('category', models.CharField(blank=True, default='Any', max_length=100, null=True)),
                ('abreviation', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=70, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(null=True, upload_to='projects/')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('level', models.CharField(blank=True, max_length=15, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=70, null=True)),
                ('url', models.CharField(max_length=22, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('views', models.IntegerField(default=0)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Module')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Project'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comentary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='No text')),
                ('likes', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('is_question', models.BooleanField(default=False)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('likes', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comentary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Comentary')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Lesson')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='players.Player')),
            ],
        ),
    ]
