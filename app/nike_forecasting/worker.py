from celery import Celery
from nike_forecasting.utils import config

global_settings = config.Settings()

# Creates an app worker
app = Celery(
    'celery_web',
    broker='pyamqp://guest@localhost//',
    backend=global_settings.redis_url,
    include=['nike_forecasting.tasks']
)
