# Generated by Django 5.1.6 on 2025-02-25 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yt_learning', '0009_videos_bhashalu'),
    ]

    operations = [
        migrations.AddField(
            model_name='bashalu',
            name='code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
