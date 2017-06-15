#! coding:utf-8

from __future__ import absolute_import

import os

from celery.schedules import crontab
# from kombu import Queue

os.system('mkdir -p /tmp/celery/backend_results')

CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_EXCHANGE = 'OSS_PARTNER_EXCHANGE'
CELERY_DEFAULT_EXCHANGE_TYPE = 'direct'
CELERY_DEFAULT_QUEUE = "FIND_PARTNER_QUEUE"

CELERYBEAT_SCHEDULE = {
    'find_partner_every_week': {
        'task': 'find_partner.agent.crontab_find_partners',
        'schedule': crontab(day_of_week=[0, 3])
    }
}

# CELERT_QUEUES = (
#     Queue('mq1', exchange='OSS_PARTNER_EXCHANGE', routing_key='mq1'),
#     Queue('mq2', exchange='OSS_PARTNER_EXCHANGE', routing_key='mq2'),
# )

AMQP_URL = 'amqp://test:test@1727.0.0.1//'
BACK_END_URL = 'file:///tmp/celery/backend_results'
DB_OSS_PARTNER_URL = 'mysql://root:root@127.0.0.1:3306/database'
DB_OSS_NOTIFY_URL = 'mysql://root:root@127.0.0.1:3306/database'
