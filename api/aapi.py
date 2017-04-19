#!-*-encoding:utf8-*-
import logging
from flask import Blueprint, request, jsonify
try:
    import simplejson as json
except:
    import json

bp = Blueprint('msg_push',__name__)
lg = logging.getLogger('/tmp/push_aapi.log')
from msg_push import send_tasks


@bp.route('/test')
def test():

    return jsonify({"code":0})


@bp.route('/oss_push/send_mail',methods=['POST'])
def send_mail():
    try:
        code = 0
        msg = "ok"
        #print dir(request)
        #print "*"*40

        r_data = request.get_data()
        lg.info(r_data)
        send_tasks.send_mail.delay(json.loads(r_data))

    except Exception,e:
        code = 1
        msg = "error"

    return jsonify({"code":code, "msg":msg})