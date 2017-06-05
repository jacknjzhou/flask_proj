#!-*-encoding:utf8-*-
from __future__ import absolute_import

import time
import traceback

from flask_mail import Message

from msg_push.celery import app
from msg_push.celery import mail

try:
    import simplejson as json
except:
    import json

from celery.task import Task
from celery.utils.log import get_task_logger
from flask import current_app

from msg_push.c_tools import validate_mail_addr
from msg_push.push_proc.app_push import APPPush
from msg_push.push_proc.sms_push import SendSMS

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
def send_mail(self,r_data={}):
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
            time.sleep(0.5)
    except Exception as e:
        traceback.print_exc()
        return self.retry(exc=e,countdown=5)
        #return False
    return True


@app.task(base=OutputTask,bind=True,max_retries=3)
def send_app_info(self,r_data={}):
    """function:"""
    try:
        r_args = []
        r_kwargs = {
            "appPushHost":current_app.config.get('APPPUSH_HOST'),
            "appPushUrl":current_app.config.get("APPPUSH_URL")
        }
        APPPush(*r_args,**r_kwargs).run(r_data)

    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e,countdown=3)
        return False
    return True


@app.task(base=OutputTask,bind=True,max_retries=3)
def send_sms(self,r_data={}):
    try:
        r_args = []
        r_kwargs = {
            "smsSysHost": current_app.config.get('SMSSYS_HOST'),
            "smsSysUrl": current_app.config.get("SMSSYS_URL")
        }
        SendSMS(*r_args,**r_kwargs).run(r_data)

    except Exception as e:
        print traceback.format_exc()
        return self.retry(exe=e,countdown=3)
    return True


@app.task(base=OutputTask,bind=True,max_retries=3)
def div_zero(self,x,y):
    try:
        print x/y

    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e,countdown=3)
        return False
    return True
