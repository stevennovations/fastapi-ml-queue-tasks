from nike_forecasting.worker import app
from celery.utils.log import get_task_logger
from nike_forecasting.prediction import predict
import redis

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


@app.task(name='nike_forecasting.predict_forecast')
def predict_forecast(date_str: str):
    """Prediction task that is launched when the worker is ran.

    Args:
        date_str (str): date string value with the format YYYYmmdd

    Returns:
        (str): Returns OK when finished
    """
    prediction = predict(date_str)
    celery_log.info(app.conf.result_backend)
    rds = redis.from_url(app.conf.result_backend)
    rds.set(f'forecast-prediction:{date_str}',
            prediction)
    celery_log.info("Celery task completed!")
    return 'OK'
