#!-*-encoding:utf8-*-
from __future__ import absolute_import

import time
import traceback

from busi_route.celery import app

try:
    import simplejson as json
except:
    import json

from celery.task import Task
from celery.utils.log import get_task_logger
from flask import current_app

logger = get_task_logger(__name__)


class OutputTask(Task):

    def on_success(self,retval,task_id,args,kwargs):
        print "task done:{0}".format(retval)
        return super(OutputTask, self).on_success(retval,task_id,args,kwargs)
    def on_failure(self,exc,task_id,args,kwargs,einfo):
        print "task fail,reason:{0}".format(exc)
        return super(OutputTask,self).on_failure(exc,task_id,args,kwargs,einfo)

    def after_return(self,status,retval,task_id,args,kwargs,einfo):
        #print "after return,status:{0}".format(status)
        return super(OutputTask,self).after_return(status,retval,task_id,args,kwargs,einfo)



@app.task(base=OutputTask,bind=True,max_retries=3)
def busi_route(self,r_data={}):
    """function:"""
    try:
        r_args = []
#        r_kwargs = {
#            "appPushHost":current_app.config.get('APPPUSH_HOST'),
#            "appPushUrl":current_app.config.get("APPPUSH_URL")
#        }
        #start processing request
        print r_data
    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e,countdown=3)
        return False
    return True

