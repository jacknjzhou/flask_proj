#!-*-encoding:utf8-*-
from __future__ import absolute_import

import traceback

from monitor_alarm.celery import app

try:
    import simplejson as json
except:
    import json

from celery.task import Task
# from celery.utils.log import get_task_logger
from flask import current_app
from utils.mylog import MyLog
from utils.influxdb_helper import InfluxDBHelper

# logger = get_task_logger(__name__)
lg = MyLog('monitor_alarm')


class OutputTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print "[]task done:{0}".format(retval)
        return super(OutputTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print "[]task fail,reason:{0}".format(exc)
        return super(OutputTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # print "after return,status:{0}".format(status)
        return super(OutputTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


@app.task(base=OutputTask, bind=True, max_retries=3)
def monitor_alarm(self, r_data={}):
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
        influxdb_obj = InfluxDBHelper(r_kwargs.get("influx_host",None),r_kwargs.get("influx_port",None),
                                      r_kwargs.get("influx_user",None),r_kwargs.get("influx_pwd",None),
                                      r_kwargs.get("influx_dbname",None))
        f_info = process_write_info_format(r_data)
        if isinstance(f_info,dict):
            f_info = [f_info]
        result = influxdb_obj.write_info(f_info)
        if not result:
            result = influxdb_obj.write_info(f_info)
        # start processing request
        # logger.info("ss")
        #lg.info(json.dumps(r_data))
        # print r_data
    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e, countdown=3)
        return False
    return result

def process_write_info_format(r_info):
    """function:"""
    f_info = {"measurement":"monitor_info"}
    f_info["tags"] ={
        "caller":r_info.get("caller"),
        "callee":r_info.get("callee")
    }
    f_info['time'] = r_info.get("startTime")

    f_info['fields']={}
    for key,value in r_info.items():
        if key not in ("caller","callee","startTime"):
            f_info['fields'][key]=value

    return f_info
