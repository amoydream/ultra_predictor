# Generated by Django 2.2.6 on 2019-10-25 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='runner',
            name='first_name',
            field=models.CharField(default='Name', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='runner',
            name='last_name',
            field=models.CharField(default='Name', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='runner',
            unique_together={('first_name', 'last_name', 'birth_year')},
        ),
        migrations.RemoveField(
            model_name='runner',
            name='name',
        ),
    ]
