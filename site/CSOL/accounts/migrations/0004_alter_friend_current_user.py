# Generated by Django 3.2 on 2021-05-26 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210522_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friend',
            name='current_user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='accounts.profile', verbose_name='Пользователь'),
        ),
    ]
