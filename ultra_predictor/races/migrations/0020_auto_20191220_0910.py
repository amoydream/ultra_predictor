# Generated by Django 2.2.6 on 2019-12-20 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('races', '0019_auto_20191220_0910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predictionrace',
            name='race_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]