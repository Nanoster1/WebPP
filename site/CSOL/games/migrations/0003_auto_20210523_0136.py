# Generated by Django 3.2 on 2021-05-22 20:36

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20210522_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='games.creatorcompany', verbose_name='Компания'),
        ),
        migrations.AlterField(
            model_name='game',
            name='image',
            field=models.ImageField(blank=True, storage=django.core.files.storage.FileSystemStorage(location=None), upload_to='games/images', verbose_name='Иконка'),
        ),
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
