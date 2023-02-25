from .worker import app
from celery.utils.log import get_task_logger
from .prediction import predict

# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)

@app.task(name='nike_forecasting.predict_forecast')
def predict_forecast(date_str :str):
    content = predict(date_str)
    celery_log.info(f"Celery task completed!")
    return content