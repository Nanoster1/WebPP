# Generated by Django 3.2 on 2021-05-23 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210522_2327'),
        ('games', '0004_auto_20210523_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorgame',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile', verbose_name='Автор'),
        ),
    ]