# -*- coding: utf-8 -*-

import requests
import logging

from simplejson import dumps

from .json import _default

HTTP_GET = "GET"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"


class RestRequest(object):
    def __init__(self, host, method=HTTP_GET, json_encode=True):
        self.host = host
        self.method = method
        self.resp = None
        self.json_encode = json_encode

    def get_url(self, uri):
        return self.host + uri

    def fetch(self, uri, headers={}, **data):
        url = self.get_url(uri)

        if self.method == HTTP_GET:
            resp = requests.get(url, params=data, headers=headers, allow_redirects=True, verify=False)
        elif self.method == HTTP_POST or self.method == HTTP_PUT:
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            if self.json_encode:
                headers["Content-Type"] = "application/json"
                data = dumps(data, default=_default)
            if self.method == HTTP_POST:
                resp = requests.post(url, data=data, headers=headers, allow_redirects=True, verify=False)
            else:
                resp = requests.put(url, data=data, headers=headers, allow_redirects=True, verify=False)
        elif self.method == HTTP_DELETE:
            resp = requests.delete(url, headers=headers, allow_redirects=True, verify=False)

        msg = "[%s] %s %s %d" % (self.method, resp.url, data, resp.status_code)
        logging.debug(msg)

        self.resp = resp

    @property
    def ok(self):
        return self.resp.status_code == 200

    @property
    def data(self):
        return self.resp.json()

    @property
    def status_code(self):
        return self.resp.status_code
