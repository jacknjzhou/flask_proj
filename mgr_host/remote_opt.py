#!-*-coding:utf8-*-
"""
@function:包装连接远程机器,并进行下发执行脚本/命令的统一方式
"""
import paramiko
import traceback


class RemoteOpt(object):
    """function:包装"""
    def __init__(self,host,port,name,pwd):
        self._host = host
        self._port = port
        self._name = name
        self._pwd = pwd
        self._conn = None
        self._trans_conn = None

    def _connect(self):
        """function:create connection"""
        try:
            conn =  paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(self._host,self._port,self._name,self._pwd)

        except Exception as e:
            print str(e)
            print traceback.format_exc()
            conn = None
        return conn

    def _ftp_connect(self):
        """function:connection as ftp type for uploading file to remote host"""
        try:
            #t = paramiko.Transport(self._host,self._port)
            #t.connect(username=self._name,password=self._pwd)
            t = self._connect()
            conn = paramiko.SFTPClient.from_transport(t.get_transport())

        except Exception as e:
            print traceback.format_exc()
            print str(e)
            conn = None
        return conn

    def __del__(self):
        if self._conn:
            print "close conn ..."
            self._conn.close()
        if self._trans_conn:
            print "close trans_conn ..."
            self._trans_conn.close()

    def exe_command(self,cmd_str=""):
        """function:connect remote host ,and execute command"""
        try:
            if self._conn is None:
                self._conn = self._connect()
            result =True
            stdin,stdout,stderr = self._conn.exec_command(cmd_str)
            msg = ''.join(stdout.readlines())
            error = ''.join(stderr.readlines())

        except Exception as e:
            result = False
            msg = ""
            error = str(e)
            print traceback.format_exc()
        return result,msg,error

    def upload_file(self,local_path="/tmp/",remote_path="/tmp/"):
        try:
            if self._trans_conn is None:
                self._trans_conn = self._ftp_connect()
            print "*****************"
            print local_path
            print remote_path
            self._trans_conn.put(local_path,remote_path)

            result = True
            msg = "OK"
            error = ""
        except Exception as e:
            print traceback.format_exc()

            error = str(e)
            result = False
            msg = ""

        return result,msg+error

if __name__ == '__main__':
    host = "127.0.0.1"
    port =2222
    username = 'vagrant'
    pwd = 'vagrant'

    obj = RemoteOpt(host,port,username,pwd)
    command_str = 'ls /vagrant'

    #result,msg,error = obj.exe_command(command_str)
    #print result
    #print msg
    #print error

    #result,msg,error = obj.upload_file('/tmp/8888.log','/vagrant/9999.log')
    #print result
    #print msg
    #print error