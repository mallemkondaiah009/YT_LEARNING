# Generated by Django 5.1.6 on 2025-03-15 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yt_learning', '0011_videoprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeHiveLogos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(null=True, upload_to='codehive_logo/')),
            ],
        ),
    ]
