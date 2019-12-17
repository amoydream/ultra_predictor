import pandas as pd
from .tools import MONTHS

class PredictionDataPreparation:
    def __init__(self, **kwargs):
        self.best_ten_run_in_hours = kwargs.get("best_ten_run_in_hours")
        self.sex = kwargs.get("sex")
        self.month = kwargs.get("month")
        self.runner_age = kwargs.get("runner_age")
        self.itra_point = kwargs.get("itra_point")
        self.distance = kwargs.get("distance")
        self.food_point = kwargs.get("food_point")
        self.time_limit = kwargs.get("time_limit")
        self.elevation_gain = kwargs.get("elevation_gain")
        self.elevation_lost = kwargs.get("elevation_lost")

    def to_dataframe(self):
        best_ten_run_in_hours = {"best_ten_run_in_hours": [self.best_ten_run_in_hours]}
        sex = self.sex_dict()
        runner_age = {"runner_age": [self.runner_age]}
        itra_point = {"itra_point": [self.itra_point]}
        food_point = {"food_point": [self.food_point]}
        distance = {"distance": [self.distance]}
        time_limit = {"time_limit": [self.time_limit]}
        elevation_gain = {"elevation_gain": [self.elevation_gain]}
        elevation_lost = {"elevation_lost": [self.elevation_lost]}

        merged_dict = {
            **best_ten_run_in_hours,
            **sex,
            **runner_age,
            **itra_point,
            **food_point,
            **time_limit,
            **elevation_gain,
            **elevation_lost,
            **distance,
        }

        for m in MONTHS:
            merged_dict[m] = 1 if m == self.month else 0

        df = pd.DataFrame(data=merged_dict)

        return df

    def sex_dict(self):
        return {"W": [int(self.sex == "w")], "M": [int(self.sex == "m")]}
