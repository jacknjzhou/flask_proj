#!-*-encoding:utf8-*-
import re
import traceback
import time
import datetime

def validate_mail_addr(email):
    """function:check email address"""
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return True
    return False


times = 2


def retry(func):
    """function:only support one return:flag is true or false"""

    def _decorator(*args, **kwargs):
        try:
            for i in range(0, times):
                print("[%s]execute time:%s" % (str(func.__name__), str(i)))
                result = func(*args, **kwargs)
                if not result:
                    time.sleep(2)
                    print("[%s]execute failure,sleep 2 seconds,continue..." % (str(func.__name__)))
                    continue
                else:
                    print("[%s]execute success..." % (str(func.__name__)))
                    return True
            # if final execute here,return failure
            print("[%s]retry %d times,execute failure,exit..." % (str(func.__name__), times))
            return False
        except:
            print("[except][decorator][%s]execute failure" % str(func.__name__))
            print(traceback.print_exc())
            return False

    return _decorator


def retry_merge(func):
    """function:support two return: result and detail"""

    def _decorator(*args, **kwargs):
        try:
            for i in range(0, times):
                print("[%s]execute time:%s" % (str(func.__name__), str(i)))
                (result, msg) = func(*args, **kwargs)
                if not result:
                    time.sleep(2)
                    print("[%s]execute failure,sleep 2 seconds retry,continue..." % (str(func.__name__)))
                    continue
                else:
                    print("[%s]execute success..." % (str(func.__name__)))
                    return (True, msg)
            # if final execute here,return failure
            print("[%s]execute failure,exit..." % (str(func.__name__)))
            return (False, "[decorator]failure more times")
        except:
            print("[except][decorator][%s]execute failure" % str(func.__name__))
            print(traceback.print_exc())
            return (False, "[decorator]except failure")

    return _decorator


def time2stamp(timestr, format_type='%Y-%m-%d %H:%M:%S'):
    return time.mktime(time.strptime(timestr, format_type))


def stamp2time(stamp, format_type='%Y-%m-%d %H:%M:%S'):
    return time.strftime(format_type, time.localtime(stamp))


def str_to_timestamp(timestr=""):
    '''function:把字符串格式的日期时间,转换成时间戳'''
    try:
        date_time = datetime.datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
    except ValueError, e:
        print e
        date_time = datetime.datetime.strptime(stamp2time(time.time(), "%Y-%m-%d") + " " + timestr, '%Y-%m-%d %H:%M:%S')

    return time.mktime(date_time.timetuple())


if __name__ == '__main__':
    print str_to_timestamp("03:30:00")
    print time.time()