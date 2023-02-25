from celery.utils.log import get_task_logger
import xgboost as xgb
import pandas as pd
from datetime import datetime
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

FEATURES = ['dayofweek', 'quarter', 'month',
            'year', 'dayofyear', 'day']


def load_model():
    """_summary_

    Returns:
        _type_: _description_
    """
    celery_log.info(ROOT_DIR)
    loaded_reg = xgb.XGBRegressor()
    loaded_reg.load_model(os.path.join(ROOT_DIR, "assets/model_sklearn.txt"))

    return loaded_reg


def create_features(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['day'] = df.index.day

    return df


def validate(date_text):
    """_summary_

    Args:
        date_text (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        date_val = datetime.strptime(date_text, '%Y%m%d')

    except ValueError:
        date_val = None
        celery_log.exception("Incorrect data format, should be YYYYmmdd")
    return date_val


def predict(date_str: str):
    """_summary_

    Args:
        date_str (str): _description_

    Returns:
        _type_: _description_
    """
    date_val = validate(date_str)
    date_val = date_val.strftime('%Y-%m-%d')
    loaded_reg = load_model()
    index = pd.date_range(date_val, date_val, freq='D')
    df = pd.DataFrame(index=index)
    unseen_test = create_features(df)

    prediction = loaded_reg.predict(unseen_test[FEATURES])
    celery_log.info(f'Prediction Result: {prediction}')
    celery_log.info('Predict task completed')
    return str(prediction[0])
