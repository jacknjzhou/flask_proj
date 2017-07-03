#!-*-encoding:utf8-*-
from __future__ import absolute_import

import os

# from celery.schedules import crontab
from kombu import Queue, Exchange


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[JustShareCloud]'
    FLASKY_MAIL_SENDER = 'JustShareCloud Admin <server@justsharecloud.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'server@justsharecloud.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # mail server config
    TITLE_DESC = u'即享云'
    # celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 600
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.monitor_alarm'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'
    CELERY_IGNORE_RESULT = True

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_LOG_FILE = '/tmp/celery_monitor_alarm_log.log'

    CELERY_QUEUES = (
        Queue('oss.notify.monitor.alarm', Exchange('oss.monitor.alarm'), routing_key='oss.monitor.alarm'),
    )
    CELERY_ROUTES = {
        'monitor_alarm.task_proc.monitor_alarm': {'queue': 'oss.notify.monitor.alarm', 'routing_key': 'oss.monitor.alarm'},
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


class AwsTestingConfig(Config):
    # mail config
    # TESTING = True
    DEBUG = True

    # celery config
    BROKER_URL = 'amqp://test:OSAxMzoxMDo0OCBDU1QgMjAxN@10.0.6.106:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


class ProductionConfig(Config):
    # celery config
    BROKER_URL = 'amqp://justshare:uoeawMfmzp81nsB-nblc@10.0.6.106:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config
    INFLUXDB_HOST = '127.0.0.1'
    INFLUXDB_PORT = 8086
    INFLUXDB_DBNAME = 'monitor_alarm'


config = {
    'development': DevelopmentConfig,
    'testing': AwsTestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
