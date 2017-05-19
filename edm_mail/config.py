#!-*-encoding:utf8-*-
from __future__ import absolute_import
#from celery.schedules import crontab
from kombu import Queue, Exchange
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[JustShareCloud]'
    FLASKY_MAIL_SENDER = 'JustShareCloud Admin <msg@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'msg@example.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #mail server config
    MAIL_SERVER = 'mail.example.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    TITLE_DESC = u'Flask Admin'
    #celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 600
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.edm_mail'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_LOG_FILE = '/tmp/proj.log'

    CELERY_QUEUES = (
        Queue('oss.notify.send.edm.mail', Exchange('oss.send.edm.mail'), routing_key='oss.send.edm.mail'),
        Queue('oss.notify.send.request', Exchange('oss.send.request'), routing_key='oss.send.request'),
        Queue('oss.notify.process.send', Exchange('oss.process.send'), routing_key='oss.process.send'),
    )
    CELERY_ROUTES = {
        'edm_mail.send_tasks.send_edm_mail': {'queue': 'oss.notify.send.edm.mail', 'routing_key': 'oss.send.edm.mail'},
        'edm_mail.send_tasks.send_request': {'queue': 'oss.notify.send.request', 'routing_key': 'oss.send.request'},
        'edm_mail.send_tasks.process_send': {'queue': 'oss.notify.process.send', 'routing_key': 'oss.process.send'}
    }
    #
    R_SECRET_INFO = 'poZFo5gtTgmmYlWLfmgNWzunEdNGBhhelzYrJPIBWjlkYAejKiqz9MuG'
    #user system config
    USRSYS_SECRET_KEY = 'example'
    USRSYS_API_URL_GET_ADMIN_CONTACT = '/usersystem/Info/v1'
    USRSYS_API_URL_GET_EMPLOYEE_CONTACT = '/usersystem/ContactInfo/v1'
    #notify config
    NOTIFY_API_URL = '/oss/api'
    #analysis config
    ANALYSIS_API_URL_SEARCH_COMPANY = '/oss/search_company'
    #sms config
    SMS_API_URL_SENDSMS = '/usersystem/sms/v1'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    #TESTING = True
    DEBUG = False
    #celery config
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp/edm_mail_result'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    NOTIFY_API_HOST = '127.0.0.1'

    USRSYS_SECRET_KEY = 'secret'
    USRSYS_API_HOST = '127.0.0.1'

    ANALYSIS_API_HOST = '127.0.0.1'

    SMS_API_HOST = '127.0.0.1'

class TestingConfig(Config):
    #mail config
    #TESTING = True
    DEBUG = True

    #celery config
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    BACKEND_URL = 'file:///tmp'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    NOTIFY_API_HOST = '127.0.0.1'

    USRSYS_SECRET_KEY = 'secret'
    USRSYS_API_HOST = '127.0.0.1'

    ANALYSIS_API_HOST = '127.0.0.1'

    SMS_API_HOST = '127.0.0.1'


class ProductionConfig(Config):
    # celery config
    
    BROKER_URL = 'amqp://guest:guest@localhost:5672//'
    BACKEND_URL = 'file:///tmp/edm_mail_result'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    NOTIFY_API_HOST = '127.0.0.1'

    USRSYS_SECRET_KEY = 'secret'
    USRSYS_API_HOST = '127.0.0.1'

    ANALYSIS_API_HOST = '127.0.0.1'

    SMS_API_HOST = '127.0.0.1'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
