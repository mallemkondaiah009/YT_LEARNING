# Generated by Django 5.1.6 on 2025-03-18 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yt_learning', '0017_alter_category_icon_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
