import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class LinearPredictor:
    def __init__(self):
        model_is_ready = False

