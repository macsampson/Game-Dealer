# Generated by Django 2.1 on 2018-08-17 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_deals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='cover_url',
            field=models.CharField(default='N/A', max_length=500),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='deal',
            name='link',
            field=models.CharField(max_length=500),
        ),
    ]
