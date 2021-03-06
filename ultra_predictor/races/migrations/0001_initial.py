# Generated by Django 2.2.6 on 2019-10-21 14:10

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRace',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('distance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('race_type', models.CharField(choices=[('f', 'Flat'), ('m', 'Mountain')], default='o', max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PredictionRace',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('start_date', models.DateField()),
                ('distance', models.DecimalField(decimal_places=2, max_digits=6)),
                ('elevation_gain', models.PositiveIntegerField()),
                ('elevation_lost', models.PositiveIntegerField()),
                ('itra', models.PositiveIntegerField()),
                ('itra_race_id', models.PositiveIntegerField()),
                ('food_point', models.PositiveIntegerField()),
                ('time_limit', models.DecimalField(decimal_places=1, max_digits=10)),
                ('itra_download_status', models.CharField(choices=[('U', 'Unready'), ('R', 'Ready'), ('S', 'Started'), ('C', 'Completed'), ('F', 'Failure')], default='U', max_length=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PredictionRaceGroup',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Runner',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('birth_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1900)])),
                ('sex', models.CharField(choices=[('m', 'Man'), ('w', 'Woman'), ('o', 'Other')], default='o', max_length=1)),
            ],
            options={
                'unique_together': {('name', 'birth_year')},
            },
        ),
        migrations.CreateModel(
            name='PredictionRaceResult',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_result', models.DurationField()),
                ('prediction_race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_race_results', to='races.PredictionRace')),
                ('runner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_race_results', to='races.Runner')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='predictionrace',
            name='prediction_race_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='races', to='races.PredictionRaceGroup'),
        ),
        migrations.CreateModel(
            name='HistoricalRaceResult',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_result', models.DurationField()),
                ('historical_race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_race_results', to='races.HistoricalRace')),
                ('runner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_race_results', to='races.Runner')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
