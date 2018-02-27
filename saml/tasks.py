from __future__ import absolute_import, unicode_literals
from celery import Celery

@app.task
def add(x, y):
    return x + Y