# Generated by Django 5.1.3 on 2024-12-16 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_rename_reader_instance_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
