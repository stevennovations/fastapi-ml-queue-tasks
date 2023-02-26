# FastAPI Sales Forecasting API

![fastapi-redis](/img/architecture.png)

## Project Description

This sample app demonstrates a prediction API that uses an XGBoost Model. It is implemented with Celery distributed task queues on top of RabbitMQ broker for prediction. API request comes through FastAPI and it is being processed asynchronously by Celery. There is a separate API endpoint to check task status. Multiple requests can be initiated and processed at the same time in parallel. Celery tasks can be monitored using Flower monitoring tool. Once the task prediction finishes it saves the forecast on redis cache that when the request is re-requested will be sent to the user as response.

* Celery [documentation](https://docs.celeryproject.org/en/stable/index.html)
* [Flower](https://flower.readthedocs.io/en/latest/) - Celery monitoring tool

## Project File Structure

```
├── Dockerfile
├── deployment.yml
├── app
│   ├── endpoint.py
│   ├── router.py
│   ├── gunicorn_config.py
│   ├── models - data models used throughout the app
│   │   └── data_models.py
│   ├── nike_forecasting - main worker folder
│   │   ├── __init__.py
│   │   ├── assets
│   │   │   └── model_sklearn.txt
│   │   ├── prediction.py
│   │   ├── tasks.py
│   │   ├── utils - utilities scripts
│   │   │   ├── config.py
│   │   │   ├── log_config.py
│   │   │   └── redis.py
│   │   └── worker.py
│   └── tests
│       └── locusts_tests.py
├── notebooks
│   └── Nike_Forecast_Modeling_Notebook.ipynb
└── requirements.txt
```

## Pre-requisite Installed Applications

These are the applications that need to be installed within your environment before you execute the commands for the application.

* Redis
* Flower
* Celery

### Environment Variables
Environment variables to setup which are important for your `config.py` settings.

```
ENVIRONMENT= <environment for your project 'dev' default>
TESTING= <0 or 1>
REDIS_URL= <localhost url of your redis server>
REDIS_PASSWORD= <password for your url> (in reality this will be moved as a secret in secrets manager)
REDIS_DB= <name of your redis db>
REDIS_TEST_KEY= <the test key of your db>
WEBSERVER= <name of your webserver>
```

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