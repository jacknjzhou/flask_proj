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
@ 平台消息推送的处理逻辑：
@    oss_notify数据库中 notify_platform_send_msg表中取提交过来的任务,进行处理
@    oss_notify数据库中 notify_platform_send_msg_detail中记录上一个处理中的详情,
@    即把所有的批量任务拆分成原子的操作.
@    转换批量任务为原子任务,组合好相应的需要发送的消息内容,放入 notify_platform_send_msg_detail中,
@    另外的定时任务单独去处理需要该表中的需要发送的任务
"""


class PlatformMessageProcess(object):
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

        return result

    def _filter_empl_info(self, empl_info_list=[]):
        """function:过滤用户系统查询出来的用户信息"""
        try:
            userid_list = [int(item.get("userId")) for item in empl_info_list if
                           item and item.get("userId") not in ("", None, "0")]
        except Exception, e:
            print(traceback.format_exc())
            userid_list = []

        return userid_list

    def _process_partly_company_push(self, info={}):
        """function:推送指定的企业"""
        # step-1:根据输入的企业查询对应的员工列表信息
        r_companyidlist = info.get("companyIdList", [])
        try:
            result = True
            msg = "OK"
            for item in r_companyidlist:
                r_comp_empl_info = self._usr_system.fetch_company_people_info(item)
                if r_comp_empl_info:
                    # 若获取的企业员工信息列表不空
                    r_usrid_list = self._filter_empl_info(r_comp_empl_info)
                    if not r_usrid_list:
                        print("[PlatformMessageProcess][_process_partly_company_push]find company[%s]platform user is null" % (str(item)))
                        continue
                    # 增加企业接收者信息
                    r_plaininfo = info.get("params", {}).get("plainInfo", {})
                    r_plaininfo['userIdList'] = r_usrid_list
                    r_plaininfo['companyId'] = item
                    r_plaininfo['companyIdList'] = [item]
                    # 重新设置其中的字段内容
                    info['sendFlag'] = 2
                    # info['companyIdList'] = r_plaininfo.get("companyIdList", [])

                    info['params']['plainInfo'] = r_plaininfo
                    # 开始写原子任务
                    w_result, w_code = self.write_atom_task_detail_info(
                        {"title": info.get("title", ""), "content": info.get("content", ""),
                           "params": info.get("params", {}),
                           "operator": info.get("operator", ""), "status": 0, "sendFlag": info.get("sendFlag", 2),
                           "companyIdList": info.get("companyIdList", []),
                           "mailAddrList": info.get("mailAddrList", [])})
                    if not w_result:
                        print("[PlatformMessageProcess]write atom task info fail:%s" % (json.dumps(info)))
                    time.sleep(0.1)
                else:
                    print("[PlatformMessageProcess]can not find company [%s] empl info." % (str(item)))
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
                   "operator": info.get("operator", ""), "status": 0, "sendFlag": info.get("sendFlag", 3),
                   "mailAddrList": info.get("mailAddrList"), "companyIdList": info.get("companyIdList", [])})
            time.sleep(0.1)
        return True

    def write_atom_task_detail_info(self, r_data ={}):
        """function:记录拆分之后的原子任务列表"""
        try:
            result = True
            code = 0
            #TODO:add send info into execute queues
            from edm_mail import send_tasks
            send_tasks.process_send.delay(r_data)
        except Exception, e:
            print(str(e))
            print traceback.format_exc()
            result = False
            code = 1

        return result, code
