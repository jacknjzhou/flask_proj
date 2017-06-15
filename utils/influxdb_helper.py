#!-*-encoding:utf8-*-
import influxdb
import traceback
#from utils.mylog import MyLog
#lg = MyLog('monitor_alarm')

class InfluxDBHelper(object):
    def __init__(self, ip, port, username, password, dbname):
        self._dbname = dbname
        self._host = ip
        self._port = port if isinstance(port, int) else int(port)
        self._username = username if username else None
        self._password = password if password else None
        #self._conn = self._connect()

    def _connect(self):
        try:
            print self._username
            print self._password
            print self._dbname
            print self._host
            print self._port

            if self._username is not None and self._password is not None:
                print "username is not none"
                conn = influxdb.InfluxDBClient(database=self._dbname, host=self._host, port=self._port,
                                               username=self._username, password=self._password)
            else:
                print "username is none"
                conn = influxdb.InfluxDBClient(database=self._dbname, host=self._host, port=self._port)

        except Exception as e:
            print str(e)
            print traceback.format_exc()
            conn = None

        return conn

    def write_info(self,json_info):
        try:
            self._conn = self._connect()
            print type(json_info)
            print json_info
            result = self._conn.write_points(json_info)

        except Exception as e:
            print str(e)
            print traceback.format_exc()
            result = False
        return result

    def query_info(self,query_str):
        """function:"""
        self._conn = self._connect()
        resp_info = self._conn.query(query_str)

        resp_info = self.parse_result(resp_info)
        return resp_info

    def parse_result(self,resp_info):
        f_result = []
        if not isinstance(influxdb.resultset.ResultSet):
            print "return result not ResultSet object."
            return f_result
        for item in resp_info.get_points():
            f_result.append(item)

        return f_result

