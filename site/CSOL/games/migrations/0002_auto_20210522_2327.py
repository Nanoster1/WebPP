# Generated by Django 3.2 on 2021-05-22 18:27

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorcompany',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=None), upload_to='games/company', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(storage=django.core.files.storage.FileSystemStorage(location=None), upload_to='games/images', verbose_name='Иконка'),
        ),
    ]