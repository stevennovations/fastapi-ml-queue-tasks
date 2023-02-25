from fastapi import APIRouter, HTTPException
from models.data_models import Task, Result
from nike_forecasting.tasks import predict_forecast
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
from nike_forecasting.prediction import validate
from fastapi import Request
import json

forecast_router = APIRouter()


@forecast_router.get('/')
def touch():
    """Function to ping and check the application

    Returns:
        str:returns 'API is running' value
    """
    return 'API is running'


@forecast_router.get('/forecast/', response_model=Task, status_code=202)
async def invoke_prediction(date_str: str):
    """_summary_

    Args:
        date_str (str): date string value with the format YYYYmmdd

    Returns:
        json: the json object from the task
    """
    if validate(date_str) is None:
        raise HTTPException(status_code=422, detail="Wrong date format: \
                            YYYYmmdd (ex. 20220923)")
    task_id = predict_forecast.delay(date_str)
    return {'task_id': str(task_id), 'status': 'Processing',
            'content': {'sample_prediction': 0}}


@forecast_router.get('/test-point/', response_model=Task, status_code=202)
async def test_endpoint(date_str: str, request: Request):
    """_summary_

    Args:
        date_str (str): date string value with the format YYYYmmdd

    Returns:
        json: the json object from the task
    """
    # print(request.app)
    # json_content = {'task_id': str(date_str), 'status': 'Processing'}
    # await request.app.state.redis.set(f'testing:{date_str}',
    #                                   json.dumps(json_content))
    prefix_url = 'forecast-prediction'
    content = await request.app.state.redis.get(f'{prefix_url}:{date_str}')
    print(content)
    content = json.loads(content)
    return {'task_id': str(date_str), 'status': 'Processing',
            'content': {'sample_prediction': content}}


@forecast_router.get('/result/{task_id}', response_model=Result,
                     status_code=200,
                     responses={202: {'model': Task,
                                      'description': 'Accepted: Not Ready'}})
async def fetch_result(task_id):
    """
    Fetching the result of the previous tasks

    Args:
        task_id (str): the task uuid of the value

    Returns:
        json: the json object of the prediction
    """
    # Fetch result for task_id
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id),
                                                      'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': str(result)}
