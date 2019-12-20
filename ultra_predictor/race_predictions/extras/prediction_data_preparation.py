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
        self.refreshment_points = kwargs.get("refreshment_points")
        self.max_time = kwargs.get("max_time")
        self.ascent = kwargs.get("ascent")
        self.descent = kwargs.get("descent")

    def to_dataframe(self):
        best_ten_run_in_hours = {"best_ten_run_in_hours": [self.best_ten_run_in_hours]}
        sex = self.sex_dict()
        runner_age = {"runner_age": [self.runner_age]}
        itra_point = {"itra_point": [self.itra_point]}
        refreshment_points = {"refreshment_points": [self.refreshment_points]}
        distance = {"distance": [self.distance]}
        max_time = {"max_time": [self.max_time]}
        ascent = {"ascent": [self.ascent]}
        descent = {"descent": [self.descent]}

        merged_dict = {
            **best_ten_run_in_hours,
            **sex,
            **runner_age,
            **itra_point,
            **refreshment_points,
            **max_time,
            **ascent,
            **descent,
            **distance,
        }

        for m in MONTHS:
            merged_dict[m] = 1 if m == self.month else 0

        df = pd.DataFrame(data=merged_dict)

        return df

    def sex_dict(self):
        return {"W": [int(self.sex == "w")], "M": [int(self.sex == "m")]}
