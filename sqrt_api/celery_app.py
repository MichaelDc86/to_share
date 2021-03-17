"""Модуль celery"""
from celery import Celery

from config import CONFIG
from logger import LOGGER

app = Celery('sqrt', include=['tasks'])
app.config_from_object(CONFIG['celery'])
app.logger = LOGGER

app.control.purge()
app.autodiscover_tasks()
