#!-*-encoding:utf8-*-
import os
import sys
import logging

_basedir = os.path.abspath(os.path.dirname(__file__))
if _basedir not in  sys.path:
    sys.path.insert(0,_basedir)

import api

from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware
#from utils import factory
from utils.logger import MyTimedRotatingFileHandler
from api.configs import LOG_PATH, DEBUG, LOG_HANDLER, SERVER_IP, SERVER_PORT

handler = MyTimedRotatingFileHandler(LOG_PATH, "midnight", 1)
formatter = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(levelname)s - %(message)s'
handler.setFormatter(logging.Formatter(formatter))
level = logging.DEBUG if DEBUG else logging.INFO
logger = logging.getLogger(LOG_HANDLER)
logger.setLevel(level)
logger.addHandler(handler)

operation_handler = MyTimedRotatingFileHandler('/tmp/push_svr_op.log', "midnight", 1)
operation_formatter = '%(asctime)s - %(name)s - %(message)s'
operation_handler.setFormatter(logging.Formatter(operation_formatter))
logger = logging.getLogger('operation')
logger.setLevel(logging.INFO)
logger.addHandler(operation_handler)


app = DispatcherMiddleware(api.create_app())

if __name__ == '__main__':
    run_simple(SERVER_IP, SERVER_PORT, app, use_reloader=DEBUG, use_debugger=DEBUG)