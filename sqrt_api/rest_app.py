"""Модуль запуска REST-api приложения"""
import json

from celery.result import AsyncResult
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool

from tasks import task_get_sqrt
from utils import validate_number

app = FastAPI()


@app.get(path="/sqrt",
         status_code=200,
         description='Endpoint to count sqrt from big digits')
async def get_sqrt(number: str) -> json:
    """
    Ручка вычисления корня из числа
    Args:
        number: str - введенное пользователем число

    Returns:
        str - джейсон-строка с ответом
    """
    number = validate_number(number)
    task = task_get_sqrt.delay(number=number)
    res = AsyncResult(task.id)
    return await run_in_threadpool(res.get)
