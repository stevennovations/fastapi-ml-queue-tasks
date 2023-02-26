# FastAPI Sales Forecasting API

![fastapi-redis](/img/architecture.png)

This sample app demonstrates a prediction API that uses an XGBoost Model. It is implemented with Celery distributed task queues on top of RabbitMQ broker for prediction. API request comes through FastAPI and it is being processed asynchronously by Celery. There is a separate API endpoint to check task status. Multiple requests can be initiated and processed at the same time in parallel. Celery tasks can be monitored using Flower monitoring tool. Once the task prediction finishes it saves the forecast on redis cache that when the request is re-requested will be sent to the user as response.


* Celery [documentation](https://docs.celeryproject.org/en/stable/index.html)
* [Flower](https://flower.readthedocs.io/en/latest/) - Celery monitoring tool

## Commands (executed from celery-web folder)

* Start FastAPI endpoint
  * **uvicorn endpoint:app --reload**
* Start Celery worker
  * **celery -A nike_forecasting.worker worker --loglevel=INFO**
* Start Flower monitoring dashboard
  * **celery -A nike_forecasting.worker --broker=pyamqp://guest@localhost// flower**

## URL's

* API url: http://127.0.0.1:8000/api/v1/nikesalesforecast/docs
* Flower url: http://127.0.0.1:5555/tasks