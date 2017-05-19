#!-*-encoding:utf8-*-
from __future__ import  absolute_import
from edm_mail.celery import app
from edm_mail.celery import mail
from flask_mail import Message

import random
import time
import traceback

try:
    import simplejson as json
except:
    import json

from celery.task import Task
from celery.utils.log import get_task_logger
from flask import current_app
from msg_push.c_tools import validate_mail_addr

from edm_mail.platform_msg.platform_message_process import PlatformMessageProcess
from edm_mail.platform_msg.platform_message_process_detail import PlatformMessageDetailProcess

logger = get_task_logger(__name__)


class OutputTask(Task):

    def on_success(self,retval,task_id,args,kwargs):
        print "task done:{0}".format(retval)
        return super(OutputTask, self).on_success(retval,task_id,args,kwargs)
    def on_failure(self,exc,task_id,args,kwargs,einfo):
        print "task fail,reason:{0}".format(exc)
        return super(OutputTask,self).on_failure(exc,task_id,args,kwargs,einfo)

    def after_return(self,status,retval,task_id,args,kwargs,einfo):
        print "after retrun,status:{0}".format(status)
        return super(OutputTask,self).after_return(status,retval,task_id,args,kwargs,einfo)


@app.task(base=OutputTask,bind=True,max_retries=3)
def send_edm_mail(self,r_data={}):
    """
    @ function:process send mail use plugin flask-mail
    @ r_data = {"RecvList":[],"Title":"","Content":""}
    """
    try:
        if not isinstance(r_data, (dict,)):
            print "input content is not dict."
            return False

        s_mail_user_desc = current_app.config.get('TITLE_DESC','Admin')
        s_mail_username = current_app.config.get("MAIL_USERNAME","")

        r_user_list = r_data.get("RecvList",[])
        r_title = r_data.get("Title","Notify")
        r_content = r_data.get("Content","")
        r_recv_list = [item for item in r_user_list if validate_mail_addr(item)]

        for item in r_recv_list:
            if isinstance(item,list):
                msg = Message(r_title,sender=(s_mail_user_desc,s_mail_username),recipients=item)
            else:
                msg = Message(r_title,sender=(s_mail_user_desc,s_mail_username),recipients=[item])
            #
            msg.html = r_content
            mail.send(msg)
            print "send message to:%s"%(item)
            logger.info(item)
            #time.sleep(0.5)
    except Exception as e:
        traceback.print_exc()
        return self.retry(exc=e,countdown=5)
    return True


@app.task(base=OutputTask,bind=True)
def send_request(self,r_data={}):
    try:
        r_args = []
        r_kwargs = {"secretKey":current_app.config.get('USRSYS_SECRET_KEY'),
                    "secretInfo":current_app.config.get('R_SECRET_INFO'),
                    "userHost":current_app.config.get('USRSYS_API_HOST'),
                    "getalladmincontactinfo":current_app.config.get('USRSYS_API_URL_GET_ADMIN_CONTACT'),
                    "getallemployeecontactinfo":current_app.config.get('USRSYS_API_URL_GET_EMPLOYEE_CONTACT'),
                    "analysis.host":current_app.config.get('ANALYSIS_API_HOST'),
                    "analysis.url.searchcompany":current_app.config.get('ANALYSIS_API_URL_SEARCH_COMPANY')}
        print json.dumps(r_kwargs)
        PlatformMessageProcess(*r_args,**r_kwargs).run(r_data)
    except Exception as e:
        traceback.print_exc()
        return self.retry(exc=e,countdown=5)
    return True


@app.task(base=OutputTask,bind=True,max_retries=3)
def process_send(self,r_data = {}):
    """function:处理发送平台系统公告"""
    try:
        #
        r_args = []
        r_kwargs = {"notifyHost":current_app.config.get("NOTIFY_API_HOST"),
                    "notifyUrl":current_app.config.get("NOTIFY_API_URL")
                    }
        PlatformMessageDetailProcess(*r_args,**r_kwargs).run(r_data)
    except Exception as e:
        print traceback.format_exc()
        return self.retry(exc=e,countdown=5)
    return True