#!-*-encoding:utf8-*-
try:
    import simplejson as json
except:
    import json

from edm_mail.ptools.http_helper import HttpHelper

'''
@ function:处理oss_analysis 接口查询任务.
'''


class AnalysisHelper(object):
    def __init__(self, *args, **kwargs):
        self._http_obj = HttpHelper(*args,**kwargs)

        self._analysis_api_host = kwargs.get("analysis.host", "")
        self._analysis_api_searchcompany = kwargs.get("analysis.url.searchcompany", "")

    def search_company_request(self, req_params={}):
        """function:发送消息通知"""
        (result, resp_data) = self._http_obj.call_external_api(self._analysis_api_host,
                                                               self._analysis_api_searchcompany,
                                                               req_params)
        return result, resp_data

    def request_params(self, **kwargs):
        """function:组合参数"""
        req_info = {"search": kwargs.get("search", ""), "page_size": kwargs.get("page_size", 50),
                    "page_number": kwargs.get("page_number", 1)}
        return req_info

    def judge_over_loop_end(self, page_size=50, info_detail=[]):
        """function:判断获取列表的循环是否可以结束"""
        if len(info_detail) < page_size:
            # 循环结束 否则继续
            return True
        return False

    def for_send_platform_msg(self, page_size=50, page_number=1, search_str=""):
        """function:"""
        req_params = self.request_params(**{"search": search_str, "page_size": page_size, "page_number": page_number})
        (result, resp_data) = self.search_company_request(req_params)
        if not result:
            print("[AnalysisHelper]call oss_analysis interface info failure:pagesize:%s,page_number:%s" % (str(page_size), str(page_number)))
            return True, []
        r_detail = resp_data.get("companyList", [])
        end_flag = self.judge_over_loop_end(page_size, r_detail)
        return end_flag, r_detail
