import pandas as pd
import joblib
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from django.conf import settings
from .tools import MONTHS
import os

import logging

logger = logging.getLogger(__name__)

from django.conf import settings


class LinearPredictor:
    def __init__(self, **kwargs):
        self.df = None
        self.model_is_ready = False
        self.X, self.y = None, None
        self.columns = None
        self.model_file_name = kwargs.get("model_file_name", "linear_model")

    def prediction(self, predictor):
        if not self.model_was_created():
            self.create_model()
        self.load_model()
        predictor = predictor.to_dataframe()[list(self.columns)]
        prediction = self.model.predict(predictor)

        return float(list(prediction)[0][0])

    def model_was_created(self):
        return os.path.exists(
            settings.PREDICTION_ML_FOLDER + "/" + self.model_file_name + ".joblib"
        )

    def create_model(self):
        self.preprocessing()
        self.train_model()
        self.model_is_ready = True

    def load_model(self):
        self.model, self.columns = joblib.load(
            settings.PREDICTION_ML_FOLDER + "/" + self.model_file_name + ".joblib"
        )

    def load_file(self):
        file = f"/{settings.PREDICTION_ML_FOLDER}/{settings.CSV_FILE_ALL_NAME_TEMPLATE}.csv"
        return file

    def preprocessing(self):
        df = self.get_data_frame()

        df.dropna(subset=["best_ten_run_in_hours"], inplace=True)
        # remove outstanding
        df = df[(np.abs(stats.zscore(df["best_ten_run_in_hours"])) < 3)]
        df = df[(np.abs(stats.zscore(df["time_result_in_hours"])) < 3)]

        dummy_sex = pd.get_dummies(df["runner_sex"])
        df = pd.concat([df, dummy_sex], axis=1)

        dummy_month = pd.get_dummies(df["month_of_the_race"])
        df = pd.concat([df, dummy_month], axis=1)

        months_to_add = list(MONTHS.intersection(set(df.columns)))
        X = df[
            months_to_add
            + [
                "M",
                "W",
                "best_ten_run_in_hours",
                "runner_age",
                "itra_point",
                "food_point",
                "time_limit",
                "distance",
                "elevation_gain",
                "elevation_lost",
            ]
        ]
        y = df[["time_result_in_hours"]]
        self.X, self.y = X, y
        return (X, y)

    def train_model(self):

        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=201
        )
        self.create_folder_for_file()
        lm = LinearRegression()
        lm.fit(X_train, y_train)
        joblib.dump(
            (lm, X_train.columns),
            settings.PREDICTION_ML_FOLDER + "/" + self.model_file_name + ".joblib",
            compress=True,
        )
        logger.info("Joblib file created")

    def get_data_frame(self):
        if not self.df:
            df = pd.read_csv(self.load_file())
            self.df = df

        return self.df

    def create_folder_for_file(self):
        try:
            os.makedirs(settings.PREDICTION_ML_FOLDER, exist_ok=True)
            logger.info("Creating folder".format(settings.PREDICTION_ML_FOLDER))
        except IOError as e:
            logger.error(
                "Error creating folder: {} with error {}".format(
                    settings.PREDICTION_ML_FOLDER, e.message
                )
            )

