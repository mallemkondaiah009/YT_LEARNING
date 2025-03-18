# Generated by Django 5.1.6 on 2025-03-18 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yt_learning', '0016_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='category_icons/'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
