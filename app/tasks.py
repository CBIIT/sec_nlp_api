from . import celery
from flask import current_app

@celery.task(name='app.tasks.add_together')
def add_together(*args, **kwargs):
    app = current_app._get_current_object()
    return args[0] + args[1]