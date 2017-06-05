#!-*-encoding:utf8-*-
from __future__ import absolute_import

import os

# from celery.schedules import crontab
from kombu import Queue, Exchange


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Example]'
    FLASKY_MAIL_SENDER = 'Flask Admin <server@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'server@example.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # mail server config
    TITLE_DESC = u'Flask Title'
    # celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 600
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.busi_route'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'
    CELERY_IGNORE_RESULT = True

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_LOG_FILE = '/tmp/celery_busi_route_log.log'

    CELERY_QUEUES = (
        Queue('oss.notify.busi.route', Exchange('oss.busi.route'), routing_key='oss.busi.route'),
    )
    CELERY_ROUTES = {
        'busi_route.task_proc.busi_route': {'queue': 'oss.notify.busi.route', 'routing_key': 'oss.busi.route'},
    }

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
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


class ProductionConfig(Config):
    # celery config
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
