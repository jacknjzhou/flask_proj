#!-*-encoding:utf8-*-
from __future__ import absolute_import

import os

# from celery.schedules import crontab
from kombu import Queue, Exchange


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[JustShareCloud]'
    FLASKY_MAIL_SENDER = 'Cloud Admin <server@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'server@example.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # mail server config
    TITLE_DESC = u'MgrHost'
    # celery public config
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TASK_RESULT_EXPIRES = 60
    CELERY_ACCEPT_CONTENT = ['json', 'msgpack']

    CELERY_DEFAULT_EXCHANGE = 'oss.mgr_host'
    # CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
    # CELERY_DEFAULT_QUEUE = 'oss.partner.default'
    CELERY_IGNORE_RESULT = False

    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ENABLE_UTC = False
    CELERY_LOG_FILE = '/tmp/celery_mgr_host_log.log'

    CELERY_QUEUES = (
        #Queue('oss.notify.mgr.host', Exchange('oss.mgr.host'), routing_key='oss.mgr.host'),
        #Queue('oss.notify.mgr.fileupload', Exchange('oss.mgr.fileupload'), routing_key='oss.mgr.fileupload'),
        Queue('oss.notify.mgr.cache.selected.file', Exchange('oss.mgr.cache.selected.file'), routing_key='oss.mgr.cache.selected.file'),
        Queue('oss.notify.mgr.publish.selected.file', Exchange('oss.mgr.publish.selected.file'), routing_key='oss.mgr.publish.selected.file'),
        Queue('oss.notify.mgr.query.publish.result', Exchange('oss.mgr.query.publish.result'), routing_key='oss.mgr.query.publish.result'),
        Queue('oss.notify.mgr.git.command', Exchange('oss.mgr.git.command'), routing_key='oss.mgr.git.command'),
        Queue('oss.notify.mgr.dir.list.file', Exchange('oss.mgr.dir.list.file'), routing_key='oss.mgr.dir.list.file'),
        Queue('oss.notify.mgr.git.branch.list', Exchange('oss.mgr.git.branch.list'), routing_key='oss.mgr.git.branch.list'),
    )
    CELERY_ROUTES = {
        #'mgr_host.task_proc.mgr_host': {'queue': 'oss.notify.mgr.host', 'routing_key': 'oss.mgr.host'},
        #'mgr_host.task_proc.mgr_fileupload': {'queue': 'oss.notify.mgr.fileupload', 'routing_key': 'oss.mgr.fileupload'},
        'mgr_host.task_proc.cache_selected_file': {'queue': 'oss.notify.mgr.cache.selected.file', 'routing_key': 'oss.mgr.cache.selected.file'},
        'mgr_host.task_proc.publish_selected_file': {'queue': 'oss.notify.mgr.publish.selected.file', 'routing_key': 'oss.mgr.publish.selected.file'},
        'mgr_host.task_proc.query_publish_result': {'queue': 'oss.notify.mgr.query.publish.result', 'routing_key': 'oss.mgr.query.publish.result'},
        'mgr_host.task_proc.execute_git_command': {'queue': 'oss.notify.mgr.git.command', 'routing_key': 'oss.mgr.git.command'},
        'mgr_host.task_proc.list_module_file': {'queue': 'oss.notify.mgr.dir.list.file', 'routing_key': 'oss.mgr.dir.list.file'},
        'mgr_host.task_proc.fetch_git_branch_list': {'queue': 'oss.notify.mgr.git.branch.list', 'routing_key': 'oss.mgr.git.branch.list'},

    }
    #add influxdb config info
    INFLUXDB_HOST = '127.0.0.1'
    INFLUXDB_PORT = 8086
    INFLUXDB_DBNAME = 'mgr_host'
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
    CELERY_RESULT_BACKEND = 'amqp://guest:guest@localhost:5672//'
    #result_backend ='rpc://'
    result_persistent=False
    #BACKEND_URL = 'file:///tmp/celery_backend_result'
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


class TestingConfig(Config):
    # mail config
    # TESTING = True
    DEBUG = True

    # celery config
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    #BACKEND_URL = 'file:///tmp'
    CELERY_RESULT_BACKEND = 'amqp://test:test@127.0.0.1:5672//'
    result_persistent = False
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config


class ProductionConfig(Config):
    # celery config
    BROKER_URL = 'amqp://test:test@127.0.0.1:5672//'
    #BACKEND_URL = 'file:///tmp'
    CELERY_RESULT_BACKEND = 'amqp://test:test@127.0.0.1:5672//'
    result_persistent = False
    # CELERY_RESULT_BACKEND='redis://localhost:6379/1'
    # app.push.api config
    INFLUXDB_HOST = '127.0.0.1'
    INFLUXDB_PORT = 8086
    INFLUXDB_DBNAME = 'mgr_host'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
