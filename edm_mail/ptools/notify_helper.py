#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json

from edm_mail.ptools.http_helper import HttpHelper

'''
@ function:处理oss_notify发送请求任务.
'''


class NotifyHelper(object):
    def __init__(self,*args,**kwargs):
        self._http_obj = HttpHelper()

        self._notify_api_host = kwargs.get("notifyHost", "")
        self._notify_api_url = kwargs.get("notifyUrl", "")

    def send_notify_request(self, req_params={}):
        """function:发送消息通知"""
        (result, resp_data) = self._http_obj.call_external_api(self._notify_api_host,
                                                               self._notify_api_url,
                                                               req_params)

        return result, resp_data

    def compse_request_content(self, method="", data={}):
        """function:每次只发一个"""
        tmp_content = {
            "params": {
                "content": {
                    "header": {
                        "key": "",
                        "module": "",
                        "operator": "PushSvr"
                    },
                    "body": {
                        "method": method,
                        "data": data
                    }
                }
            }
        }
        return tmp_content

    def process_resp(self, resp_data={}):
        """function:处理调用接口成功之后的解析"""
        if resp_data.get("errorCode") in ("0", 0):
            return True
        return False
