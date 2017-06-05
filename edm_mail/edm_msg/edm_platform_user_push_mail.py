#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json
import traceback
import time
import re
import datetime
from edm_mail.c_tools import str_to_timestamp

from edm_mail.ptools.usrsys_helper import UserSystemHelper
from edm_mail.ptools.analysis_helper import AnalysisHelper


"""
@ function:
@ 向已注册的平台用户推送营销邮件处理逻辑：
"""


class EDMPlatformMailProcess(object):
    def __init__(self, *args, **kwargs ):
        self._usr_system = UserSystemHelper(*args,**kwargs)
        self._analysis_obj = AnalysisHelper(*args,**kwargs)

    def run(self,data = {}):
        # start process task
        self.process_send_flag(data)

    def process_send_flag(self, info={}):
        """function:根据输入的sendFlag进行处理"""
        if info.get("sendFlag", 0) == 1:
            # all platform company push info
            result = self._process_all_platform_push(info)
        elif info.get("sendFlag", 0) == 2:
            result = self._process_partly_company_push(info)
        elif info.get("sendFlag", 0) == 3:
            result = self._process_mail_push(info)
        else:
            result = True
        return result

    def _filter_empl_info(self, empl_info_list=[]):
        """function:过滤用户系统查询出来的用户信息"""
        try:
            user_mail_list = [item.get("email") for item in empl_info_list if
                           item and item.get("email") not in ("", None)]
        except Exception, e:
            print(traceback.format_exc())
            user_mail_list = []

        return user_mail_list

    def _process_partly_company_push(self, info={}):
        """function:推送指定的企业"""
        # step-1:根据输入的企业查询对应的员工邮件信息
        r_companyidlist = info.get("companyIdList", [])
        try:
            result = True
            msg = "OK"
            for item in r_companyidlist:
                r_comp_empl_info = self._usr_system.fetch_company_people_info(item)
                if r_comp_empl_info:
                    # 若获取的企业员工信息列表不空
                    r_usr_mail_list = self._filter_empl_info(r_comp_empl_info)
                    if not r_usr_mail_list:
                        print("[PlatformMessageProcess][_process_partly_company_push]find company[%s]platform user is null" % (str(item)))
                        continue
                    # 增加企业接收者信息
                    r_plaininfo = info.get("params", {}).get("plainInfo", {})
                    r_plaininfo['companyId'] = item
                    r_plaininfo['mailAddrList'] = r_usr_mail_list
                    # 重新设置其中的字段内容
                    info['sendFlag'] = 3
                    # info['companyIdList'] = r_plaininfo.get("companyIdList", [])
                    r_mail_addr_list = info.get("mailAddrList",[])
                    if r_mail_addr_list:
                        if isinstance(r_mail_addr_list,(list,)):
                            info['mailAddrList'].extend(r_usr_mail_list)
                        elif isinstance(r_mail_addr_list,(str,unicode)):
                            info['mailAddrList'] = r_usr_mail_list
                            info['mailAddrList'].append(r_mail_addr_list)
                        else:
                            info['mailAddrList'] = r_usr_mail_list
                    else:
                        info['mailAddrList'] = r_usr_mail_list
                    #end
                    info['params']['plainInfo'] = r_plaininfo
                    # 开始写原子任务
                    print json.dumps(info)
                    w_result, w_code = self._process_mail_push(
                        {"title": info.get("title", ""), "content": info.get("content", ""),
                           "params": info.get("params", {}), "companyIdList": info.get("companyIdList", []),
                           "mailAddrList": info.get("mailAddrList", [])})
                    if not w_result:
                        print("[EDMPlatformMailProcess]write atom task info fail:%s" % (json.dumps(info)))
                    time.sleep(0.1)
                else:
                    print("[EDMPlatformMailProcess]can not find company [%s] empl info." % (str(item)))
        except Exception, e:
            msg = "Occur error."
            print(str(e))
            print(traceback.format_exc())
            result = False
        return result

    def _process_all_platform_push(self, info={}):
        """function:全平台推送--复用指定企业发送的处理逻辑"""
        try:
            # 循环调用web_admin接口获取企业列表,并进行处理.
            page_size = 50
            cur_page_num = 1

            while True:
                end_flag, company_list_info = self._analysis_obj.for_send_platform_msg(page_size, cur_page_num)
                # TODO:
                info['companyIdList'] = [item.get("companyId") for item in company_list_info if item.get("companyId")]
                if not self._process_partly_company_push(info):
                    print("[PlatformMessage][_process_all_platform_push]process occur fail:%s" % (json.dumps(info['companyIdList'])))
                time.sleep(1)
                cur_page_num = cur_page_num + 1
                if end_flag:
                    print("[PlatformMessage][_process_all_platform_push]fetch company info over.")
                    break

            result = end_flag

        except Exception, e:
            print(str(e))
            print(traceback.format_exc())
            result = False

        return result

    def _process_mail_push(self, info={}):
        """function:处理单独推送邮件的任务(需要拆分为单个邮件进行处理)"""

        def validateEmail(email):
            """function:校验邮箱合法性"""
            if len(email) > 7:
                if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
                    return True

            print("[validateEmail]not validate mail:%s" % str(email))
            return False
        from edm_mail import send_tasks

        r_mailaddrlist = info.get("mailAddrList", [])
        if not r_mailaddrlist:
            print "[EDMPlatformMailProcess][_process_mail_push]input mail address list is null,not process."
            return True
        for index, item_mail in enumerate(r_mailaddrlist):
            if not validateEmail(item_mail):
                # 校验不通过则继续循环
                continue
            r_plaininfo = info.get("params", {}).get("plainInfo", {})
            r_plaininfo['mailAddrList'] = [item_mail]
            info['mailAddrList'] = [item_mail]
            info['sendFlag'] = 3
            # 开始写原子任务
            send_tasks.send_edm_mail.delay({"Title":info.get('title',''),
                                            "Content":info.get('content',''),
                                            "RecvList":info.get('mailAddrList',[])})

            print json.dumps({"title": info.get("title", ""),
                   "mailAddrList": info.get("mailAddrList"), "companyIdList": info.get("companyIdList", [])})
            time.sleep(0.1)
        return True
