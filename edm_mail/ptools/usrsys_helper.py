#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json
import traceback
import time
import uuid
import hashlib
from edm_mail.ptools.http_helper import HttpHelper

'''
function:user system api call process
'''


class UserSystemHelper(object):
    def __init__(self,*args,**kwargs):
        self._http_obj = HttpHelper()

        self._usr_host = kwargs.get("userHost", '127.0.0.1')
        self._usr_url_getalladmincontactinfo = kwargs.get("getalladmincontactinfo",
                                                          "/usersystem/company/getAllAdminContactInfo/v1")
        self._usr_url_getallemployeecontactinfo = kwargs.get("getallemployeecontactinfo",
                                                             "/usersystem/employee/getAllEmployeeContactInfo/v1")
        self._secret_info = kwargs.get("secretInfo","")

        self._secret_key = kwargs.get("secretKey", "zhihulian2016first")

    def gen_sign_info(self):
        '''function:generate access trans module api signature info.'''
        r_key = str(uuid.uuid4())
        r_sign = hashlib.md5(r_key + self._secret_info).hexdigest()
        return {"key": r_key, "sign": r_sign}

    def fetch_notify_people_info(self, companyId=0):
        '''function:fetch company admin contact'''
        # step-1:inner process function
        def _req_param(company_id):
            t_time = self.__gen_time_key()
            r_param = {
                "companyId": [company_id],
                "timestamp": t_time,
                "secretValue": self.__gen_secret_value(company_id, t_time)
            }
            return r_param

        # step-2:
        r_params = _req_param(companyId)
        (r_result, resp_data) = self._http_obj.call_external_api(self._usr_host, self._usr_url_getalladmincontactinfo,
                                                                 r_params)
        if not r_result:
            print('[UserSystemHelper][fetch_notify_people_info]call usersystem api error.')
            return []
        # parse response info
        print("[UserSystemHelper][fetch_notify_people_info]errorCode:%s" % (resp_data.get("errorCode", "-1")))
        print("[UserSystemHelper][fetch_notify_people_info]errorMsg:%s" % (resp_data.get("errorMsg", "unkown")))

        r_emplContact = resp_data.get("emplContact", [])
        if not r_emplContact:
            print("[UserSystemHelper][fetch_notify_people_info]can not fetch contact people info.")
            return []
        # if not null ,return first one
        return r_emplContact

    def __gen_secret_value(self, company_id=0, t_timestamp=""):
        """function:genrate secret info for call user system"""
        tmp_secret_value = ""
        if company_id <= 0:
            tmp_secret_value = str(t_timestamp) + self._secret_key
        else:
            tmp_secret_value = str(company_id) + str(t_timestamp) + self._secret_key
        # hash process
        m = hashlib.md5()
        m.update(tmp_secret_value)
        return m.hexdigest()

    def __gen_time_key(self):
        """function:get current timestamp"""
        r_timestamp = int(time.time())
        return r_timestamp

    def fetch_company_people_info(self, companyid=0):
        """function:fetch company user contact info """
        # step-1:inner process function
        def _req_param(company_id):
            t_time = self.__gen_time_key()
            r_param = {
                "companyId": company_id,
                "timestamp": t_time,
                "secretValue": self.__gen_secret_value(company_id, t_time)
            }
            return r_param

        # step-2:
        r_params = _req_param(companyid)
        (r_result, resp_data) = self._http_obj.call_external_api(self._usr_host,
                                                                 self._usr_url_getallemployeecontactinfo,
                                                                 r_params)
        if not r_result:
            print('[UserSystemHelper][fetch_company_people_info]call usersystem api error.')
            return []
        # parse response info
        print("[UserSystemHelper][fetch_company_people_info]errorCode:%s" % (resp_data.get("errorCode", "-1")))
        print("[UserSystemHelper][fetch_company_people_info]errorMsg:%s" % (resp_data.get("errorMsg", "unkown")))
        #print(str(resp_data))
        r_emplcontact = resp_data.get("emplContact", [])
        if not r_emplcontact:
            print("[UserSystemHelper][fetch_company_people_info]can not fetch contact people info.")
            return []
        elif r_emplcontact in ('[]', [], None, ""):
            print("[UserSystemHelper][fetch_company_people_info]query return info is %s" % (str(r_emplcontact)))
            return []
        else:
            pass
        # if not null ,return first one
        return r_emplcontact
