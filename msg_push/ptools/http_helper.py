# -*-encoding:utf8-*-

try:
    import simplejson as json
except:
    import json
import traceback
import httplib, urllib
from msg_push.ptools.c_tools import retry_merge


class HttpHelper():
    def __init__(self,*args,**kwargs):
        self._timeout = kwargs.get("timeout",30)

    @retry_merge
    def call_external_api(self, host_and_port, url, params):
        print "call external api:", host_and_port, url, params
        ret_flag = True
        data = ""
        headers = {"Content-type": "application/x-www-form-urlencoded",
                   "Accept": "text/plain"}
        try:
            req_data = json.dumps(params)
            conn = httplib.HTTPConnection(host_and_port, timeout=self._timeout)
            conn.request("POST", url, req_data, headers)
            response = conn.getresponse()
            # output("[external api]response:(%s,%s)"%(str(response.status),str(response.reason)))
            data = json.loads(response.read())
            #print "*"*30
            #print json.dumps(data)
            #print "*"*30
            # output(data)
        except Exception, e:
            print(traceback.print_exc())
            ret_flag = False
            if hasattr(e, "reason"):
                data = e.reason
            elif hasattr(e, "message"):
                data = e.message
            else:
                data = "urlopen error: unknown reson."

        conn.close()
        return ret_flag, data