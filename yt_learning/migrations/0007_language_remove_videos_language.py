# Generated by Django 5.1.6 on 2025-02-23 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yt_learning', '0006_videos_language'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='videos',
            name='language',
        ),
    ]
