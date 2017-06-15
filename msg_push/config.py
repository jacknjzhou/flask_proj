#!-*-encoding:utf8-*-
from __future__ import absolute_import
#from celery.schedules import crontab
from kombu import Queue, Exchange
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Cloud]'
    FLASKY_MAIL_SENDER = 'Flask Admin <server@cloud.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'server@cloud.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #mail server config
    MAIL_SERVER = 'mail.example.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    TITLE_DESC = u'消息'
    #celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 600
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.msg_push'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'
    CELERY_IGNORE_RESULT = True

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_LOG_FILE = '/tmp/celery_msg_push_proj.log'

    CELERY_QUEUES = (
        Queue('oss.notify.send.mail', Exchange('oss.send.mail'), routing_key='oss.send.mail'),
        Queue('oss.notify.send.app', Exchange('oss.send.app'), routing_key='oss.send.app'),
        Queue('oss.notify.send.sms', Exchange('oss.send.sms'), routing_key='oss.send.sms'),
    )
    CELERY_ROUTES = {
        'msg_push.send_tasks.send_mail': {'queue': 'oss.notify.send.mail', 'routing_key': 'oss.send.mail'},
        'msg_push.send_tasks.send_app_info': {'queue': 'oss.notify.send.app', 'routing_key': 'oss.send.app'},
        'msg_push.send_tasks.send_sms': {'queue': 'oss.notify.send.sms', 'routing_key': 'oss.send.sms'}
    }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    #TESTING = True
    DEBUG = False
    #celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp/celery_backend_result'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config
    APPPUSH_HOST = '127.0.0.1:82'
    APPPUSH_URL = '/jpush/jpush/pushByAlias'
    # sms.sys.api config
    SMSSYS_HOST = '127.0.0.1'
    SMSSYS_URL = '/usersystem/sms/sendSms/v1'


class TestingConfig(Config):
    #mail config
    #TESTING = True
    DEBUG = True

    #celery config
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'


class ProductionConfig(Config):
    MAIL_SERVER = 'mail.cloud.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # celery config
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config
    APPPUSH_HOST = 'jpush.justsharecloud.com'
    APPPUSH_URL = '/jpush/jpush/pushByAlias'
    # sms.sys.api config
    SMSSYS_HOST = 'usersystem.justsharecloud.com'
    SMSSYS_URL = '/usersystem/sms/sendSms/v1'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
    
}
