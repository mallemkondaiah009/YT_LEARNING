# Generated by Django 5.1.6 on 2025-02-21 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yt_learning', '0003_videos_yt_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ImageField(null=True, upload_to='category_icons/'),
        ),
    ]
