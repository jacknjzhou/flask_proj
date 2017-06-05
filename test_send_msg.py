#!-*-encoding:utf8-*-
from msg_push import send_tasks 

#a={"RecvList":['jacknj_zhou@163.com','jacknj_zhou@126.com','284680326@qq.com'],'Title':"Test send mail.","Content":"Test send mail."}
a={"RecvList":['jacknj_zhou@163.com','284680326@qq.com'],'Title':"Test send mail.","Content":"Test send mail."}

send_tasks.send_mail.delay(a)
