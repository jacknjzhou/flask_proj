#!-*-encoding:utf8-*-
from __future__ import absolute_import

import traceback
import time
from timing_task.celery import app

try:
    import simplejson as json
except:
    import json

from celery.task import Task
# from celery.utils.log import get_task_logger
from flask import current_app
from utils.mylog import MyLog
# from utils.influxdb_helper import InfluxDBHelper
from timing_task.timing_alarm.alarm_proc import AlarmProc

# logger = get_task_logger(__name__)
lg = MyLog('timing_task')


class OutputTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print "task done:{0}".format(retval)
        return super(OutputTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print "task fail,reason:{0}".format(exc)
        return super(OutputTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # print "after return,status:{0}".format(status)
        return super(OutputTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


@app.task(base=OutputTask, bind=True, max_retries=3)
def crontab_alarm(self, r_data={}):
    """function:"""
    try:
        r_args = []
        r_kwargs = {
            "influx_host": current_app.config.get('INFLUXDB_HOST'),
            "influx_port": current_app.config.get("INFLUXDB_PORT"),
            "influx_dbname": current_app.config.get("INFLUXDB_DBNAME"),
            "influx_user": current_app.config.get("INFLUXDB_USER"),
            "influx_pwd": current_app.config.get("INFLUXDB_PWD")
        }
        lg.info(json.dumps(r_kwargs))
        result = True
        alarm_proc = AlarmProc(**r_kwargs)

        r_info = alarm_proc.process()
        lg.info(json.dumps(r_info))

    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e, countdown=3)
        return False
    return result
