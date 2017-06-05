#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json
import traceback
import time
import re

from edm_mail.ptools.notify_helper import NotifyHelper

"""
@function:实现对导入的平台潜在客户进行推送edm信息

"""


class EDMImportPersonMail(object):

    def __init__(self, *args, **kwargs):
        self._notify_obj = NotifyHelper(*args, **kwargs)


    def run(self,r_data = {}):
        """function:推送导入平台库中的客户邮件"""
        #step-1:获取客户的列表,并进行
        self._process(r_data)
        return

    def _process(self,r_data = {}):
        """function:main process"""
        i = 0
        count = 50
        from edm_mail.send_tasks import send_edm_mail
        while True:
            req_data = {"pageInfo": {"start": i, "count": count}}
            if r_data.get("sourceFlag",""):
                req_data['sourceFlag'] = r_data.get("sourceFlag")

            req_params = self._notify_obj.compse_request_content("fetchEDMMailList", req_data)

            result,resp_data = self._notify_obj.send_notify_request(req_params)
            if result:
                r_num, r_details = self._notify_obj.parse_details(resp_data)
                mail_list = self._filter_mail_list(r_details)
                if mail_list:
                    send_edm_mail.delay({"RecvList":mail_list,
                                         "Title":r_data.get("title",""),
                                         "Content":r_data.get("content","")})
                else:
                    print "Return mail is null,not process"
                #
                if r_num < count:
                    print "Return mail num less count,loop over."
                    break
            else:
                print "Call Notify API Error."
                break

            i = i + count

        return

    def _filter_mail_list(self,resp_details=[]):
        """function:过滤出来邮件列表"""
        mail_list =[item.get('email') for item in resp_details if item.get('email')]
        return mail_list
