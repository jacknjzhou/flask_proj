#!-*-encoding:utf8-*-
from __future__ import absolute_import

import os

from celery.schedules import crontab
from kombu import Queue, Exchange


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Cloud]'
    FLASKY_MAIL_SENDER = 'Admin <server@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'server@example.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # mail server config
    TITLE_DESC = u'即享云'
    # celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 600
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.timing_task'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'
    CELERY_IGNORE_RESULT = True

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_LOG_FILE = '/tmp/oss_timing_task.log'

    CELERY_QUEUES = (
        Queue('oss.timing.task.crontab', Exchange('oss.timing.task.crontab'), routing_key='oss.timing.task.crontab'),
    )
    CELERY_ROUTES = {
        'timing_task.timing_task_proc.crontab_alarm': {'queue': 'oss.timing.task.crontab', 'routing_key': 'oss.timing.task.crontab'},
    }

    CELERYBEAT_SCHEDULE = {
        'crontab_alarm': {'task': 'timing_task.timing_task_proc.crontab_alarm', 'schedule': crontab('*/1'),
                'args': ()}
    }
    #add influxdb config info
    INFLUXDB_HOST = '127.0.0.1'
    INFLUXDB_PORT = 8086
    INFLUXDB_DBNAME = 'monitor_alarm'
    #INFLUXDB_USER = None
    #INFLUXDB_PWD = None

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # TESTING = True
    DEBUG = False
    # celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp/celery_backend_result'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


class TestingConfig(Config):
    # mail config
    # TESTING = True
    DEBUG = True

    # celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


class ProductionConfig(Config):
    # celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config
    INFLUXDB_HOST = '127.0.0.1'
    INFLUXDB_PORT = 8086
    INFLUXDB_DBNAME = 'monitor_alarm'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
