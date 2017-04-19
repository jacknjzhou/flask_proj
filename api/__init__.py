#!-*-encoding:utf8-*-
import os
import sys
import logging
try:
    import simplejson as json
except:
    import json

from os.path import dirname, abspath
from voluptuous import  MultipleInvalid
from utils import factory
from utils.errors import ErrArgs, ErrSystem, AppError
#from api.configs import LOG_HANDLER
LOG_HANDLER = '/tmp_push_app.log'
lg = logging.getLogger(LOG_HANDLER)
#from wsgi import logger
#lg = logger

def create_app(settings_override=None):
    #app_name = dirname(dirname(abspath(__file__))).split(os.sep)[-1]
    app_name = 'api'
    app = factory.create_app(app_name, __name__, __path__, settings_override)

    app.errorhandler(Exception)(on_app_error)
    app.errorhandler(MultipleInvalid)(on_args_error)

    return app


def on_app_error(e):
    if not isinstance(e, AppError):
        lg.error(e.message)
        e = ErrSystem
    data = dict(code=e.code, message=e.message)
    rv = json.dumps(data)

    return rv, e.status_code


def on_args_error(e):
    return on_app_error(ErrArgs)