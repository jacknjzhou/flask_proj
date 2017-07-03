#!-*-encoding:utf8-*-
import logging
import time
from utils.logger import MyTimedRotatingFileHandler

req = time.strftime('%Y%m%d', time.localtime(time.time()))

setting = {'logpath': '/tmp/', 'filename': 'oss_push_api' + req + '.log'}

# lg_handler = None
#
# def single_instance(name):
#     global lg_handler
#     if lg_handler is None:
#         return MyLog(name)
#     return lg_handler

class MyLog(object):
    """function:wrapper log output"""
    def __init__(self,name):
        self.path = setting['logpath']
        self.filename = setting['filename']
        #self.filename = filename
        self.name = name
        self.logger = logging.getLogger(self.name)

        self.logger.setLevel(logging.DEBUG)
        #self.fh = logging.FileHandler(self.path + self.filename)
        self.fh = MyTimedRotatingFileHandler(self.path+self.filename)
        self.fh.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(name)s-%(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def close(self):
        self.logger.removeHandler(self.fh)
