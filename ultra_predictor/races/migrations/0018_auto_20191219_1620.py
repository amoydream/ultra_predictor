# Generated by Django 2.2.6 on 2019-12-19 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0017_auto_20191219_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predictionrace',
            name='time_limit',
        ),
        migrations.AddField(
            model_name='predictionrace',
            name='max_time',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='predictionrace',
            name='race_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='predictionrace',
            name='refreshment_points',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
