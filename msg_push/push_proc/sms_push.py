#!-*-encoding:utf8-*-
# @author:jerryzhou
# @summary:
# @date:2016-02-26
# @version:1.0
try:
    import simplejson as json
except:
    import json
import traceback

from msg_push.ptools.http_helper import HttpHelper


class SendSMS(object):
    """docstring for  SendMail"""

    def __init__(self, *args, **kwargs):

        self._sms_host = kwargs.get("smsSysHost", "")
        self._sms_url = kwargs.get("smsSysUrl", "")
        self._http_obj = HttpHelper(*args, **kwargs)

    def run(self, r_data={}):
        #
        try:
            print "*************[SendSMS]*********************"
            self.process(r_data)
        except Exception, e:
            print e
            traceback.print_exc()
            return False
        return True

    def process(self, r_data={}):
        '''function:处理发送消息'''
        try:
            r_mobiles = r_data.get("mobiles", [])
            r_content = r_data.get("content", "")
            #
            req_params = self._compose_req_params(r_content, r_mobiles)
            #
            (result, resp_data) = self._http_obj.call_external_api(self._sms_host,
                                                                   self._sms_url,
                                                                   req_params)
            if result:
                result = self._parse_resp(resp_data)
                print "Send Result:",result
            else:
                print "Call API Error:",resp_data
        except Exception, e:
            print traceback.format_exc()
        return

    def _compose_req_params(self, content="", mobiles=[]):
        '''function:组合参数'''
        req_params = {
            "commonParam": {
                "interfaceVersion": "1.0",
                "sourceSystem": "OSS"
            },
            "content": content,
            "mobiles": mobiles
        }

        return req_params

    def _parse_resp(self, resp_data={}):
        result = True
        if resp_data.get("errorCode", "") not in ("0", 0):
            result = False
        return result
