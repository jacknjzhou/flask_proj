#!-*-coding:utf8-*-
"""
@function:处理告警
"""
import time
import traceback

from utils.influxdb_helper import InfluxDBHelper


class AlarmProc(object):
    def __init__(self, *args, **kwargs):
        self._influx_host = kwargs.get("influx_host")
        self._influx_port = kwargs.get("influx_port")
        self._influx_user = kwargs.get("influx_user")
        self._influx_pwd = kwargs.get("influx_pwd")
        self._influx_dbname = kwargs.get("influx_dbname")

    def process(self):
        """main process"""
        try:
            influxdb_obj = InfluxDBHelper(self._influx_host, self._influx_port,
                                          self._influx_user, self._influx_pwd,
                                          self._influx_dbname)
            f_result = self.filter_rule(influxdb_obj)
        except Exception as e:
            print str(e)
            print traceback.format_exc()
            f_result = {}
        return f_result

    def filter_rule(self, influx_obj):
        """function:筛选/汇总"""
        f_result = {}
        for key, value in self.sum_rule_info_list().items():
            f_result[key] = influx_obj.query_info(value)

        return f_result

    def sum_rule_info_list(self):
        """function:需要执行的语句(统计一天内的数量)"""
        t_time = int(time.time()) - 24 * 60 * 60
        sql_info_dict = {
            "three_group": "select count(*) from monitor_info where time<now() and startTime>= {0} group by methodName,caller,callee;",
            "method_group": "select count(*) from monitor_info where time<now() and startTime>= {0} group by methodName;"
        }

        t_sql_info_dict = {}
        for key, value in sql_info_dict.items():
            t_sql_info_dict[key] = value.format(t_time)

        return t_sql_info_dict
