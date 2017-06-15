#!-*-encoding:utf8-*-
import traceback
import logging
from flask import Blueprint, request, jsonify
try:
    import simplejson as json
except:
    import json

from utils.mylog import MyLog

bp_route = Blueprint('busi_route',__name__)
bp = Blueprint('msg_push',__name__)
#lg = logging.getLogger('/tmp/push_aapi.log')
lg = MyLog('oss_api')
from msg_push import send_tasks
from monitor_alarm import task_proc


@bp_route.route('/oss_push/monitor_alarm',methods=["POST"])
def monitor_alarm():
    try:
        r_data = request.get_data()
        lg.info(r_data)
        r_data = json.loads(r_data)

        task_proc.monitor_alarm.delay(r_data)
    except Exception,e:
        print str(e)
        print traceback.print_exc()
        return jsonify({"code":1,"msg":str(e)})
    return jsonify({"code":0,"msg":"ok"})


@bp.route('/test',methods=['POST'])
def test():

    return jsonify({"code":0})


@bp.route('/oss_push/send_mail',methods=['POST'])
def send_mail():
    try:
        code = 0
        msg = "ok"
        print dir(request)
        print "*"*40

        r_data = request.get_data()
        lg.info(r_data)
        send_tasks.send_mail.delay(json.loads(r_data))

    except Exception as e:
        code = 1
        msg = "error"

    return jsonify({"code":code, "msg":msg})
