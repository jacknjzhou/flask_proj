#!-*-encoding:utf8-*-
import traceback

from flask import Blueprint, request, jsonify

try:
    import simplejson as json
except:
    import json

from utils.mylog import MyLog

#bp_route = Blueprint('monitor_alarm', __name__)
bp = Blueprint('msg_push', __name__)
bp_mgr_host = Blueprint('mgr_host', __name__)
# lg = logging.getLogger('/tmp/push_aapi.log')
lg = MyLog('oss_api')
from msg_push import send_tasks
#from monitor_alarm import task_proc
from mgr_host import task_proc as host_task_porc
from mgr_host.extra_config import module_conf_list

@bp_mgr_host.route('/oss_push/mgr_host/module_config_list', methods=['POST'])
def module_config_list():
    """function:获取已经配置的模块列表"""
    try:
        code = 0
        msg = "OK"
        details = module_conf_list

    except Exception as e:
        lg.error(traceback.format_exc())
        code = 1
        msg = str(e)
        details = []
    return jsonify({"code":code,"msg":msg,"details":details})

@bp_mgr_host.route('/oss_push/mgr_host/list_dir_file', methods=['POST'])
def list_dir_file():
    """function:展示指定模块所在目录下层级文件/文件夹列表"""

    def _check_params(r_data):
        result = True
        msg = "OK"

        if not r_data.get("module"):
            result = False
            msg = "[list_dir_file][check_param]miss param module or null."
        return result, msg

    try:
        code = 0
        msg = "OK"
        details = []
        #
        r_data = request.get_data()
        r_data = json.loads(r_data)
        result, msg = _check_params(r_data)
        if result:
            obj = host_task_porc.list_module_file.delay(r_data)
            details = obj.get(timeout=30)
            lg.info(details)
    except Exception as e:
        lg.error(traceback.format_exc())
        msg = str(e)
        code = 1
        details = []

    return jsonify({"code": code, "msg": msg, "details": details})


@bp_mgr_host.route('/oss_push/mgr_host/get_branch_list',methods=['POST'])
def get_branch_list():
    """"""
    def _check_params(r_data):
        result = True
        msg = "OK"

        if not r_data.get("module"):
            result = False
            msg = "[get_branch_list][check_param]miss param module or null."
        return result, msg

    try:
        code = 0
        msg = "OK"
        details = []
        r_data = request.get_data()
        r_data = json.loads(r_data)
        result, msg = _check_params(r_data)
        if result:
            obj = host_task_porc.fetch_git_branch_list.delay(r_data)
            msg, details = obj.get(timeout=30)
        else:
            code = 1

    except Exception as e:
        lg.error(traceback.format_exc())
        code = 1
        msg = str(e)
        details = []

    return jsonify({"code":code,"msg":msg,"details":details})


@bp_mgr_host.route('/oss_push/mgr_host/git_file_update', methods=['POST'])
def git_file_update():
    """function:下载指定模块的git目录下文件的更新"""

    def _check_params(req_data={}):
        """function:check params"""
        result = True
        msg = "OK"
        if not req_data.get("module"):
            result = False
            msg = "[git_file_update][check_param]not input module info or null."
        if not req_data.get("branch"):
            print "[git_file_update][check_param]not input branch info,update by config setting."
        return result, msg

    try:
        code = 0
        r_data = request.get_data()
        r_data = json.loads(r_data)
        result, msg = _check_params(r_data)
        if not result:
            print "[check_params]check fail."
            code = 1
        else:
            result = host_task_porc.execute_git_command.delay(r_data)
            print "start execute git command..."
            msg = result.get(timeout=30)
            print "end git command..."

    except Exception as e:
        print traceback.format_exc()
        msg = str(e)
        code = 1
    return jsonify({"code": code, "msg": msg})


@bp_mgr_host.route('/oss_push/mgr_host/query_publish_result', methods=["POST"])
def query_publish_result():
    """function:查询发布结果"""
    try:
        code = 0
        msg = "OK"

        r_data = request.get_data()
        r_data = json.loads(r_data)

        # result, info = host_task_porc.query_publish_result(r_data)
        result = host_task_porc.query_publish_result.delay(r_data)
        # print "&" * 30
        # print type(result)
        # print result.ready()
        lg.info(result.id)
        info = result.get(timeout=10)
        # lg.info(json.dumps(info))
        # while True:
        #    if result.ready():
        #        print result.get()
        #        break
        #    else:
        #        time.sleep(1)
        # print "&"*30
        # if not result:
        #    msg = "query result error."
        #    code = 1
        # info =[]
    except Exception as e:
        print traceback.format_exc()
        code = 1
        msg = str(e)
        info = []
    return jsonify({"code": code, "msg": msg, "details": info})


@bp_mgr_host.route('/oss_push/mgr_host/cache_selected_file', methods=['POST'])
def cache_selected_file():
    """function:cache selected file"""

    def _check_params(r_data={}):
        if not r_data.get("module"):
            msg = "[API][cache_selected_file][check_param]key [module] must be contains."
            return False, msg
        if not r_data.get("fileList"):
            msg = "[API][cache_selected_file][check_param]key [fileList] must be contains."
            return False, msg
        #
        if not isinstance(r_data.get("fileList"), list):
            msg = "[API][cache_selected_file][check_param]key [fileList] value type must be list."
            return False, msg
        return True, "OK"

    try:
        code = 0
        msg = "OK"
        r_data = request.get_data()
        r_data = json.loads(r_data)

        result, msg = _check_params(r_data)
        if result:
            host_task_porc.cache_selected_file.delay(r_data)
            # host_task_porc.cache_selected_file(r_data)
        else:
            print msg
            code = 1

    except Exception as e:
        print traceback.format_exc()
        msg = str(e)
        code = 1
    return jsonify({"code": code, "msg": msg})


@bp_mgr_host.route('/oss_push/mgr_host/publish_selected_file', methods=['POST'])
def publish_selected_file():
    """"""

    def _check_params(r_data={}):
        if not r_data.get("module"):
            msg = "[API][cache_selected_file][check_param]key [module] must be contains."
            return False, msg
        return True, "OK"

    try:
        code = 0
        msg = "OK"
        r_data = request.get_data()
        r_data = json.loads(r_data)

        result, msg = _check_params(r_data)
        if result:
            host_task_porc.publish_selected_file.delay(r_data)
        else:
            print msg
            code = 1

    except Exception as e:
        print traceback.format_exc()
        msg = str(e)
        code = 1
    return jsonify({"code": code, "msg": msg})


# @bp_route.route('/oss_push/monitor_alarm', methods=["POST"])
# def monitor_alarm():
#     """function:接收告警推送"""
#     try:
#         r_data = request.get_data()
#         lg.info(r_data)
#         r_data = json.loads(r_data)
#
#         task_proc.monitor_alarm.delay(r_data)
#     except Exception, e:
#         print str(e)
#         print traceback.print_exc()
#         return jsonify({"code": 1, "msg": str(e)})
#     return jsonify({"code": 0, "msg": "ok"})


@bp.route('/test', methods=['POST'])
def test():
    return jsonify({"code": 0})


@bp.route('/oss_push/send_mail', methods=['POST'])
def send_mail():
    try:
        code = 0
        msg = "ok"
        print dir(request)
        print "*" * 40

        r_data = request.get_data()
        lg.info(r_data)
        send_tasks.send_mail.delay(json.loads(r_data))

    except Exception as e:
        code = 1
        msg = "error"

    return jsonify({"code": code, "msg": msg})
