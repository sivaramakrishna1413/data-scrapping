# Generated by Django 5.1.5 on 2025-02-18 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.TextField(blank=True, null=True),
        ),
    ]
