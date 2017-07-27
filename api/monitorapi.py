#!-*-encoding:utf8-*-
import traceback
import logging
from flask import Blueprint, request, jsonify
try:
    import simplejson as json
except:
    import json

from utils.mylog import MyLog

bp_monitor_route = Blueprint('monitor_alarm',__name__)
#lg = logging.getLogger('/tmp/push_aapi.log')
lg = MyLog('oss_api')
#from msg_push import send_tasks
from monitor_alarm import task_proc


@bp_monitor_route.route('/oss_push/monitor_alarm', methods=["POST"])
def monitor_alarm():
    """function:接收告警推送"""
    try:
        r_data = request.get_data()
        lg.info(r_data)
        r_data = json.loads(r_data)

        task_proc.monitor_alarm.delay(r_data)
    except Exception, e:
        print str(e)
        print traceback.print_exc()
        return jsonify({"code": 1, "msg": str(e)})
    return jsonify({"code": 0, "msg": "ok"})


# @test_route.route('/test/route',methods=['POST'])
# def test():
#     lg.info(request.get_data())
#     return jsonify({"code":1,"msg":"test"})

