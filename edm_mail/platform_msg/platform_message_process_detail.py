#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json
import traceback
import time
from edm_mail.ptools.notify_helper import NotifyHelper


class PlatformMessageDetailProcess(object):
    """function：读oss_notify.notify_platform_send_msg_detail中的记录进行调用notify接口进行处理"""

    def __init__(self, *args, **kwargs):
        self._notify_obj = NotifyHelper(*args,**kwargs)

    def run(self, data={}):
        """function:main process"""
        try:
            # step-2:process send
            r_data = self.data_detail(data)
            (s_result, s_resp_data) = self._notify_obj.send_notify_request(
                self._notify_obj.compse_request_content("sendPlainMessage", r_data))
            if s_result:
                ft_result = self._notify_obj.process_resp(s_resp_data)
            else:
                pass
            # 短暂sleep 0.5 seconds
            time.sleep(0.5)

        except Exception, e:
            print(str(e))
            print(traceback.format_exc())
        return

    def data_detail(self,info={}):
        """
        @ function:组合请求内容中的data信息
        @ 若有格式和请求数据上的变化可以在此进行定制
        @ info的格式是从对应的表中读取的相应的信息的字典方式表示
         @仅获取其中的params字段的信息进行做为发送信息
        """
        r_data = {
            "sendCompanyName": info.get("params", {}).get("sendCompanyName", ""),
            "sendCompanyId": info.get("params", {}).get("sendCompanyId", 100),
            "plainInfo": [info.get("params", {}).get("plainInfo", {})],
            "userId": info.get("params", {}).get("sendCompanyId", 100),
        }
        return r_data
