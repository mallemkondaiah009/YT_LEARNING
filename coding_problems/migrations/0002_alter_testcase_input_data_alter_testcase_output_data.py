# Generated by Django 5.1.6 on 2025-03-19 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coding_problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='input_data',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='testcase',
            name='output_data',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
