"""Модуль вспомогательных функций"""
import decimal
from logger import LOGGER

from fastapi import HTTPException


def validate_number(number: str) -> decimal.Decimal:
    try:
        number = decimal.Decimal(number)
        if len(str(abs(number))) > 30:
            LOGGER.info('Invalid number! len number: %s is > 30, code: 422', number)
            raise HTTPException(status_code=422, detail=f'{number}: Number`s length must be < 30')
        if number < 0:
            LOGGER.info('Invalid number! number: %s is < 0, code: 422', number)
            raise HTTPException(status_code=422, detail=f'{number}: Number must be > 0')
        return number
    except decimal.InvalidOperation:
        LOGGER.info('Invalid number! number: %s is not a number, code: 422', number)
        raise HTTPException(status_code=422, detail='Invalid number')
