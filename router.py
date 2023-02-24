from fastapi import APIRouter, FastAPI, HTTPException
from models.data_models import RequestData, Task, Result
from nike_forecasting.tasks import predict_forecast
from celery.result import AsyncResult
from fastapi.responses import JSONResponse
import pandas as pd

router = APIRouter()


@router.get('/')
def touch():
    return 'API is running'

@router.post('/train', response_model=Task, status_code=202)
async def run_training(requestData:RequestData):
    task_id = predict_forecast.delay(requestData.date_str)
    return {'task_id': str(task_id), 'status': 'Processing'}

@router.get('/result/{task_id}', response_model=Result, status_code=200,
            responses={202: {'model': Task, 'description': 'Accepted: Not Ready'}})
async def fetch_result(task_id):
    # Fetch result for task_id
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(status_code=202, content={'task_id': str(task_id), 'status': 'Processing'})
    result = task.get()
    return {'task_id': task_id, 'status': str(result)}

# @router.get('/invoke')
# async def invoke(requestData:RequestData):

    
#     return JSONResponse(content, status_code=200) # or error 422 for wrong input format

# @router.get('/ping')
# async def ping():
#     return {"body": "healthy"}


# @router.post('/invocations')
# async def invocations():
#     return {"body": "prediction"}