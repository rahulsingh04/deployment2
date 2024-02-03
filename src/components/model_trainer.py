import os
import sys
sys.path.append(os.getcwd())

from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    train_model_file_path: str = os.path.join("Artifact", "model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split Training And Test Input Data :-->")
            X_train, Y_train, X_test, Y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            model_report = evaluate_models(X_train, X_test, Y_train, Y_test, models)
            logging.info(f"Model Report Are : {model_report}")

            # To get the best model score from the dict
            best_model_score = max(model_report.values())

            # To get the best model name from the dict
            best_model_name = next(key for key, value in model_report.items() if value == best_model_score)
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No Best Model Found!!!")

            logging.info("Best Model Found Is {0} and Its Accuracy is {1}".format(best_model_name, best_model_score))
            save_object(file_path=self.model_trainer_config.train_model_file_path, obj=best_model)

            predicted = best_model.predict(X_test)
            r2_square = r2_score(Y_test, predicted)
            return r2_square
        except Exception as e:
            raise CustomException(e, sys)
