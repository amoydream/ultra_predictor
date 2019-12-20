# Generated by Django 2.2.6 on 2019-12-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0009_auto_20191210_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_date',
        ),
        migrations.AddField(
            model_name='event',
            name='itra_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
