#!-*-encoding:utf8-*-
# @author:jackson
# @summary:在消息推送时候,调用封装的友盟接口
try:
    import simplejson as json
except:
    import json
import traceback
from msg_push.ptools.http_helper import HttpHelper

'''
function:调用友盟 封装接口继续APP消息推送.
能够处理的消息结构{"title":"","content":"","userId":[]}
'''


class APPPush(object):
    def __init__(self, *args, **kwargs):
        self._host = kwargs.get("appPushHost", "")
        self._url = kwargs.get("appPushUrl", "")
        self._http_obj = HttpHelper(*args,**kwargs)

    def run(self, r_data={}):
        """function:main entrance"""
        try:
            user_info = r_data.get('userList',[])
            if not user_info:
                print "enter user info is null,return."
                return True

            if isinstance(user_info,(str,unicode)):
                user_info = [user_info]

            (code, msg) = self.push_info(r_data.get("title", ""),
                                         r_data.get("content", ""),
                                         user_info,
                                         r_data.get("jsonString", {}),
                                         r_data.get("msgType", 0))
            #print code,msg
        except Exception, e:
            traceback.print_exc()
            print str(e)
            return False

        return True

    def push_info(self, title, content, person_list=[], json_str="", msg_type=0):
        """function:推送消息入口"""
        try:
            code = 0
            msg = "OK"
            req_params = self.compose_params(title, content, person_list, json_str, msg_type)

            (result, resp_data) = self._http_obj.call_external_api(self._host, self._url, req_params)
            if not result:
                code = 1
                msg = resp_data
            #
            else:
                (code, msg) = self.parse_resp_data(resp_data)
        except Exception, e:
            code = 2
            msg = str(e)
            print msg
            print traceback.print_exc()
        return (code, msg)

    def parse_resp_data(self, resp_data={}):
        """function:解析返回的结果"""
        try:
            code = int(resp_data.get("errorCode", 3))
            msg = resp_data.get("errorMsg", "") + resp_data.get("detail", "")
        except Exception, e:
            code = 2
            msg = str(e)
            print msg
            print traceback

        return (code, msg)

    def compose_params(self, title="", content="", person_list=[], json_str="", msg_type=0):
        """function:组合参数"""
        if msg_type == 0:
            return {"MsgType": msg_type, "MsgContent": content, "title": title, "aliasList": person_list}
        elif msg_type == 1:
            return {"MsgType": msg_type, "jsonString": json_str, "aliasList": person_list}
        return {}
