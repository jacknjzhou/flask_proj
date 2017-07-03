#!-*-encoding:utf8-*-
from __future__ import absolute_import
import os
import sys
import subprocess
import commands
import traceback
import time
from mgr_host.celery import app

try:
    import simplejson as json
except:
    import json

from celery.task import Task
# from celery.utils.log import get_task_logger
from flask import current_app
from utils.mylog import MyLog
from utils.influxdb_helper import InfluxDBHelper
from mgr_host.code_publish import CodePublish

from mgr_host.extra_config import module_deploy_ip_conf
from mgr_host.git_exc import GitCmd
# logger = get_task_logger(__name__)
lg = MyLog('mgr_host')


class OutputTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        #print "[]task done:{0}".format(retval)
        return super(OutputTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print "[]task fail,reason:{0}".format(exc)
        return super(OutputTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # print "after return,status:{0}".format(status)
        return super(OutputTask, self).after_return(status, retval, task_id, args, kwargs, einfo)

# @app.task(base=OutputTask,bind=True,max_retries=3)
# def git_file_download(self,r_data={}):
#     try:
#         r_module = r_data.get("module","")
#
#     except Exception as e:
#         print traceback.format_exc()
#         self.retry(exc=e,countdown=3)
#         return False
#     return True

@app.task(base=OutputTask,bind=True,max_retries=1)
def list_module_file(self,r_data={}):
    """function:指定模块,文件夹 展示本目录下的 文件,文件夹列表信息"""

    try:
        info = []
        r_module = r_data.get("module")
        r_relative_dir = r_data.get("relativeDir","")

        result,info,msg = GitCmd().list_branch_list(r_module,r_relative_dir)
        lg.info(msg)
        lg.info(info)
    except Exception as e:
        lg.error(traceback.format_exc())
        self.retry(exc=e, countdown=1)
        return []
    return info

@app.task(base=OutputTask,bind=True,max_retries=1)
def  execute_git_command(self,r_data={}):
    """function:进入指定的目录中,执行git 命令 获取相应的模块文件更新内容"""
    try:
        r_module = r_data.get("module")
        if not r_module:
            info = "[execute_git_command]input info module [%s] info null.not allowed."%(r_module,)
            return info
        #input branch info.
        r_branch = r_data.get("branch")
        if not r_branch:
            r_branch = ""

        info = "OK"
        result, info = GitCmd().fetch_branch_update(r_module,r_branch)
        #print info
    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e, countdown=1)
        return str(e)
    return info

@app.task(base=OutputTask,bind=True,max_retries=1)
def fetch_git_branch_list(self,r_data={}):
    try:
        r_module = r_data.get("module")
        if not r_module:
            info = "[fetch_git_branch_list]input info module [%s] info null.not allowed." % (r_module,)
            return info, []

        info = "OK"
        result, r_list, info = GitCmd().fetch_branch_name_list(r_module)
        # print info
    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e, countdown=1)
        return str(e),[]
    return info, r_list

@app.task(base=OutputTask,bind=True,max_retries=2)
def cache_selected_file(self,r_data = {}):
    try:
        module_info = r_data.get("module")
        file_list = r_data.get("fileList",[])
        print  module_info
        print file_list

        result,msg = CodePublish().cache_selected_file(module_info,file_list)
        print msg
        write_log_info(**{"ip":"same","module":module_info,"result":result,"errorInfo":msg})

    except Exception as e:
        lg.info(traceback.format_exc())
        self.retry(exc=e,countdown=2)
        return False
    return True

@app.task(base=OutputTask,bind=True,max_retries=2)
def publish_selected_file(self,r_data):
    try:
        r_module = r_data.get("module","")
        if not r_module:
            print "[publish_selected_file]input module info is null.not process"
            return True
        #
        r_ip_list = module_deploy_ip_conf.get(r_module)
        if r_ip_list:
            for ip in r_ip_list:
                result,msg = CodePublish().publish_selected_file(r_module,ip)
                lg.info(msg)
                write_log_info(**{"ip":ip,"module":r_module,"result":result,"errorInfo":msg})

    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e,countdown=2)
        return False
    return True

@app.task(base=OutputTask,bind=True,max_retries=1)
def query_publish_result(self,r_data):
    """"""
    try:
        r_module = r_data.get("module")
        info = []
        sql_str = "select * from publish_result_info where module='%s' and time>=%d"%(r_module,(int(time.time())-2*24*60*60)*1000000000)
        print sql_str
        result,msg,info = query_publish_info(sql_str)
        #print info
    except Exception as e:
        print traceback.format_exc()
        self.retry(exc=e,countdown=1)
        return []
    return info

# @app.task(base=OutputTask,bind=True,max_retries=3)
# def mgr_fileupload(self,r_data={}):
#     """function:指定文件上传"""
#     try:
#         #执行文件上传,并把上传之后的结果进行写入时序DB中作为查询的结果.
#         #上传目标的设备的相关用户名/密码或者 配置信息 需要单独进行存储
#         #step-1:判断文件是否存在,
#         #step-2:判断目标位置的是否可写
#         #step-3:执行写操作,并返回结果
#         pass
#     except Exception as e:
#         print traceback.format_exc()
#         self.retry(exc=e,countdown=3)
#         return False
#     return True

def query_publish_info(sql_str):
    """"""
    try:

        r_kwargs = {
            "influx_host": current_app.config.get('INFLUXDB_HOST'),
            "influx_port": current_app.config.get("INFLUXDB_PORT"),
            "influx_dbname": current_app.config.get("INFLUXDB_DBNAME"),
            "influx_user": current_app.config.get("INFLUXDB_USER"),
            "influx_pwd": current_app.config.get("INFLUXDB_PWD")
        }
        lg.info(json.dumps(r_kwargs))
        influxdb_obj = InfluxDBHelper(r_kwargs.get("influx_host", None),
                                      r_kwargs.get("influx_port", 8086),
                                      r_kwargs.get("influx_user", None),
                                      r_kwargs.get("influx_pwd", None),
                                      r_kwargs.get("influx_dbname", None))

        info = influxdb_obj.query_info(sql_str)

        result =True
        msg ="OK"
    except Exception as e:
        print traceback.format_exc()
        print str(e)
        info = []
        result =False
        msg = str(e)
    return result, msg, info

def write_log_info(**kwargs):
    """function:"""
    def process_result_info_format(**kwargs):
        f_info = {"measurement": "publish_result_info"}
        f_info["tags"] = {
            "ip": kwargs.get("ip"),
            "module": kwargs.get("module"),
            "result": kwargs.get("result")
        }
        # f_info['time'] = int(time.time())

        f_info['fields'] = {"errorInfo":kwargs.get("errorInfo")}

        return f_info

    try:
        r_kwargs = {
            "influx_host": current_app.config.get('INFLUXDB_HOST'),
            "influx_port": current_app.config.get("INFLUXDB_PORT"),
            "influx_dbname": current_app.config.get("INFLUXDB_DBNAME"),
            "influx_user": current_app.config.get("INFLUXDB_USER"),
            "influx_pwd": current_app.config.get("INFLUXDB_PWD")
        }
        #lg.info(json.dumps(r_kwargs))
        influxdb_obj = InfluxDBHelper(r_kwargs.get("influx_host",None),
                                      r_kwargs.get("influx_port",None),
                                      r_kwargs.get("influx_user",None),
                                      r_kwargs.get("influx_pwd",None),
                                      r_kwargs.get("influx_dbname",None))
        f_info = process_result_info_format(**kwargs)
        if isinstance(f_info,dict):
            f_info = [f_info]
        result = influxdb_obj.write_info(f_info)
        print result
        if not result:
            result = influxdb_obj.write_info(f_info)

    except:
        lg.info(traceback.format_exc())
        print traceback.format_exc()

    return




# @app.task(base=OutputTask, bind=True, max_retries=3)
# def mgr_host(self, r_data={}):
#     """function:"""
#     try:
#         result = True
#         r_args = []
#         pass
#         # r_kwargs = {
#         #     "influx_host": current_app.config.get('INFLUXDB_HOST'),
#         #     "influx_port": current_app.config.get("INFLUXDB_PORT"),
#         #     "influx_dbname": current_app.config.get("INFLUXDB_DBNAME"),
#         #     "influx_user": current_app.config.get("INFLUXDB_USER"),
#         #     "influx_pwd": current_app.config.get("INFLUXDB_PWD")
#         # }
#         # lg.info(json.dumps(r_kwargs))
#         # influxdb_obj = InfluxDBHelper(r_kwargs.get("influx_host",None),r_kwargs.get("influx_port",None),
#         #                               r_kwargs.get("influx_user",None),r_kwargs.get("influx_pwd",None),
#         #                               r_kwargs.get("influx_dbname",None))
#         # f_info = process_upload_result_info_format(r_data)
#         # if isinstance(f_info,dict):
#         #     f_info = [f_info]
#         # result = influxdb_obj.write_info(f_info)
#         # if not result:
#         #     result = influxdb_obj.write_info(f_info)
#         # start processing request
#         # logger.info("ss")
#         #lg.info(json.dumps(r_data))
#         # print r_data
#     except Exception as e:
#         print traceback.format_exc()
#         self.retry(exc=e, countdown=3)
#         return False
#     return result

def process_upload_result_info_format(r_info):
    """function:"""
    f_info = {"measurement":"upload_result_info"}
    f_info["tags"] ={
        "caller":r_info.get("caller"),
        "callee":r_info.get("callee"),
        "traceId":r_info.get("traceId"),
        "parentId":r_info.get("parentId"),
        "spanId":r_info.get("spanId"),
        "methodName":r_info.get("methodName")
    }
    #f_info['time'] = int(time.time())

    f_info['fields']={}
    for key,value in r_info.items():
        if key not in ("caller","callee","traceId","parentId","spanId","methodName"):
            f_info['fields'][key]=value

    return f_info
