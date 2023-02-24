from celery import Celery

app = Celery(
    'celery_web',
    broker='pyamqp://guest@localhost//',
    backend='rpc://',
    include=['nike_forecasting.tasks']
)