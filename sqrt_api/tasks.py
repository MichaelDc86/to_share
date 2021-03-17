"""Таски для Celery"""
import decimal
from typing import Dict, Any

from celery_app import app
from logger import LOGGER


@app.task(bind=True, name='sqrt.get_sqrt')
def task_get_sqrt(self, number: str) -> Dict[str, Any]:
    """
    Таска на расчет корня

    Args:
        self: celery app
        number: str - число для вычисления корня(str тк из брокера)

    Returns:
         decimal.Decimal - вычисленное значение корня
    """
    number = decimal.Decimal(number)
    res = number.sqrt()
    answer = {'input': number, 'sqrt': res.to_eng_string()}
    LOGGER.info('Sqrt evaluated! answer: %s', answer)
    return answer
