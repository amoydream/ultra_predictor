import csv
import os
from django.conf import settings

from ultra_predictor.races.models import PredictionRaceGroup, PredictionRaceResult
from decimal import Decimal, getcontext


class CsvGenerator:
    def __init__(self, **kwargs):
        self.group = kwargs.get("group")
        self.path = kwargs.get("path", settings.FOLDER_FOR_CSV)
        if self.group and not isinstance(self.group, PredictionRaceGroup):
            raise ValueError("Group should by PredictionRaceGroup class")
        self.filepath = None
        self.csv_file = None
        if self.group:
            self.csv_file = f"{settings.CSV_FILE_PREDICTION_GROUP_NAME_TEMPLATE}{self.group.id}.csv"
        else:
            self.csv_file = f"{settings.CSV_FILE_ALL_NAME_TEMPLATE}.csv"
        self.filepath = f"{self.path}/{self.csv_file}"
        os.makedirs(self.path, exist_ok=True)

        self.prepare_data()

    def rows_number(self):
        if not self.filepath:
            raise ValueError("There is no file yet")
        i = 0
        with open(self.filepath) as f:
            for i, l in enumerate(f):
                pass
        return i

    def prepare_data(self):
        if self.group:
            results = self.group.all_results_of_prediction_races()
        else:
            results = PredictionRaceResult.objects.all()    
        with open(self.filepath, mode="w+") as group_file:
            group_writer = csv.writer(
                group_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            group_writer.writerow(
                [
                    "runner_age",
                    "best_ten_run_in_hours",
                    "runner_sex",
                    "itra_point",
                    "food_point",
                    "time_limit",
                    "month_of_the_race",
                    "distance",
                    "elevation_gain",
                    "elevation_lost",
                    "time_result_in_hours",
                    "position",
                ]
            )
            for result in results:
                try:
                    best_10 = Decimal(
                        result.best_10km_run_before_prediction_race.seconds / 3600
                    )
                    best_10_rounded = round(best_10, 2)

                except AttributeError:
                    best_10_rounded = ""
                group_writer.writerow(
                    [
                        result.runner_age_during_race,
                        best_10_rounded,
                        result.runner.sex,
                        result.prediction_race.itra,
                        result.prediction_race.food_point,
                        result.prediction_race.time_limit,
                        result.prediction_race.month_of_the_race,
                        result.prediction_race.distance,
                        result.prediction_race.elevation_gain,
                        result.prediction_race.elevation_lost,
                        round(result.time_result_in_hours, 2),
                        result.position,
                    ]
                )

