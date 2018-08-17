# Generated by Django 2.1 on 2018-08-17 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_deals', '0002_auto_20180816_1844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='cover_url',
        ),
        migrations.AddField(
            model_name='deal',
            name='cover_hash',
            field=models.CharField(default='N/A', max_length=200),
            preserve_default=False,
        ),
    ]
