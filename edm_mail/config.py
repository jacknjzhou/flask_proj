#!-*-encoding:utf8-*-
from __future__ import absolute_import
#from celery.schedules import crontab
from kombu import Queue, Exchange
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[JustShareCloud]'
    FLASKY_MAIL_SENDER = 'JustShareCloud Admin <server@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'server@example.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    TITLE_DESC = u'即享云'
    #celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 600
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.msg_push'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False

    CELERY_LOG_FILE = '/tmp/celery_msg_push_proj.log'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    #TESTING = True
    DEBUG = False
    MAIL_SERVER = 'mail.example.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp/celery_backend_result'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'

    CELERY_QUEUES = (
        Queue('dev.send.mail', Exchange('dev.send.mail'), routing_key='dev.send.mail'),
    )

    CELERY_ROUTES = {
        'msg_push.send_tasks.send_mail': {'queue': 'dev.send.mail', 'routing_key': 'dev.send.mail'}
    }


class TestingConfig(Config):
    #mail config
    #TESTING = True
    DEBUG = True
    MAIL_SERVER = 'mail.example.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #celery config
    BROKER_URL = 'amqp://guest:guest@loalhost:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'

    CELERY_QUEUES = (
        Queue('test.send.mail', Exchange('test.send.mail'), routing_key='test.send.mail'),
    )

    CELERY_ROUTES = {
        'msg_push.send_tasks.send_mail': {'queue': 'test.send.mail', 'routing_key': 'test.send.mail'}
    }


class ProductionConfig(Config):
    MAIL_SERVER = 'mail.example.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'

    CELERY_QUEUES = (
        Queue('prod.send.mail', Exchange('prod.send.mail'), routing_key='prod.send.mail'),
    )

    CELERY_ROUTES = {
        'msg_push.send_tasks.send_mail': {'queue': 'prod.send.mail', 'routing_key': 'prod.send.mail'}
    }

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
