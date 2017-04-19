# -*- coding: utf-8 -*-

from datetime import datetime, date
from simplejson import dumps
from decimal import Decimal

from flask import Response

try:
    from bson import ObjectId
except ImportError:
    ObjectId = None


def _default(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, Decimal):
        return "%.2f" % obj
    elif isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError("%r is not JSON serializable" % obj)


def jsonify(args):
    resp = Response(
        dumps(args, default=_default)
    )
    resp.mimetype = 'application/json'
    return resp


def obj_to_dict(obj, filters=[]):
    _dict = dict()
    for k, v in obj.__dict__.iteritems():
        if k not in filters and not k.startswith('_'):
            _dict[k] = v

    return _dict


def obj_to_dicts(obj):
    result = None

    if isinstance(obj, list):
        result = list()
        for _ in obj:
            result.append(obj_to_dict(_, filters=['query', 'query_class']))

    return result
