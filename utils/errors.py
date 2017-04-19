# -*- coding: utf-8 -*-


class AppError(Exception):
    def __init__(self, code, message, status_code):
        self.code = code
        self.message = message
        self.status_code = status_code

    def __str__(self):
        message = self.message
        if isinstance(message, unicode):
            message = message.encode('utf-8')
        return '<%d %s>' % (self.code, message)


class ServerError(AppError):
    def __init__(self, code, message, status_code=500):
        super(ServerError, self).__init__(code, message, status_code)


class ClientError(AppError):
    def __init__(self, code, message, status_code=400):
        super(ClientError, self).__init__(code, message, status_code)


# 全局
ErrArgs = ClientError(10001, u'参数错误')
ErrSystem = ServerError(10002, u'系统错误')
ErrDataBase = ServerError(10003, u'数据库错误')
ErrRedisOpt = ServerError(10004, u'Redis操作失败')

# oss_analysis
ErrNoModel = ClientError(20001, u'此id在数据库中不存在', status_code=404)
ErrOrderType = ClientError(20002, u'此订单类型不支持')
ErrCountType = ClientError(20003, u'此统计类型不支持')

# web_admin
ErrUploadImage = ServerError(30001, u'图片上传失败')
ErrUploadAppPackage = ServerError(30002, u'app上传失败')
