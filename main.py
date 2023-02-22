from typing import Any, Dict
import os

from fastapi import Body, Request, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pytz
from datetime import datetime
import logging 
import xgboost as xgb
import sklearn
import pandas as pd

description = """
Forecasting API helps you assess the demand for a particular date. 🚀

## Forecast Date

You will be able to:

* **Get demand for specific date** (_not implemented_).
"""

logger = logging.getLogger()
app = FastAPI()

FEATURES = ['dayofweek', 'quarter', 'month',
       'year', 'dayofyear', 'day']

def load_model():
    loaded_reg = xgb.XGBRegressor()
    loaded_reg.load_model("models/model_sklearn.txt")

    return loaded_reg

loaded_reg = load_model()

def create_features(df) :
  """
  Create time series features based on time series index
  """
  # df = df.to_frame()
  df = df.copy()
  df['dayofweek'] = df.index.dayofweek
  df['quarter'] = df.index.quarter
  df['month'] = df.index.month
  df['year'] = df.index.year
  df['dayofyear'] = df.index.dayofyear
  df['day'] = df.index.day

  return df


def validate(date_text):
    try:
        date_val = datetime.strptime(date_text, '%Y%m%d')

    except ValueError:
        date_val = None
        logger.exception("Incorrect data format, should be YYYYmmdd")
    
    return date_val

@app.get('/invoke')
async def invoke(date_str: str):

    date_val = validate(date_str)
    if date_val is None:
        raise HTTPException(status_code=422, detail="Wrong date format: YYYYmmdd (ex. 20220923)")
    
    date_val = date_val.strftime('%Y-%m-%d')

    index = pd.date_range(date_val, date_val, freq = 'D')
    df = pd.DataFrame(index = index)
    unseen_test = create_features(df)

    prediction = loaded_reg.predict(unseen_test[FEATURES])
    print(prediction)


    content = {"body": "healthy", "date" : date_val, "prediction" : str(prediction[0])}
    return JSONResponse(content, status_code=200) # or error 422 for wrong input format

@app.get('/ping')
async def ping():
    return {"body": "healthy"}


@app.post('/invocations')
async def invocations():
    return {"body": "prediction"}