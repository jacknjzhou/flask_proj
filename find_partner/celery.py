#! coding:utf-8

from __future__ import absolute_import
from celery import Celery

from find_partner.config import AMQP_URL, BACK_END_URL

app = Celery('find_partner',
             broker=AMQP_URL,
             backend=BACK_END_URL,
             include=['find_partner.agent'])
app.config_from_object('find_partner.config')

if __name__ == '__main__':
    app.start()
