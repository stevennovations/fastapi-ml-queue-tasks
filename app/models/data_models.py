from pydantic import BaseModel


class RequestData(BaseModel):
    """ Request data Model
    """
    date_str: str


class Task(BaseModel):
    """ Task data Model
    """
    # Celery task representation
    task_id: str
    status: str
    content: dict


class Result(BaseModel):
    """ Result data Model
    """
    # Celery task result
    task_id: str
    status: str
