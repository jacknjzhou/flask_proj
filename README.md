# flask_proj
flask相关的实践内容
主要包括了相关的flask第三方插件的使用
flask-sqlalchemy
flask-login
flask-script
等

# 邮件推送(Flask+Celery方式Python实现)

##背景
>之前采用多线程方式使用stmplib库,进行推送邮件消息,总会出现时序错乱的情况,抛出RCPT的异常,初步断定可能和使用此库的线程池不安全有一定的关系,现使用了Celery+Flask进行了重写邮件推送部分的后端实现,使用了Flask-Mail插件库进行推送邮件,进行替换现有方式.

##功能定位
>仅提供邮件等消息的推送,不做其他的业务逻辑处理(纯后端处理).

##代码结构
>git项目目录: flask_proj  (现在仅使用到<strong>msg_push</strong>, 另一个待后续使用)

##启动方式
>1.开发调试方式 celery worker -A msg_push -l info
>2.supervisor方式管理,配置文件参考如下(supervisor的部署和配置文件解释,请参考相应文档)
```
[program:msg_push]
command=/{virtual_env}/bin/celery -A msg_push worker  --loglevel=info
redirect_stderr=true
stdout_logfile=/tmp/msg_push.log
stdout_logfile_maxbytes=5MB
stdout_logfile_backups=10
directory=/{code_path_dir}/flask_proj
user={run_user}
```
注释:以上字段,需要根据环境进行做相应的配置调整

##调用方式
>1.需要在相应的调用模块中导入msg_push模块(加入到服务所在的环境变量变量配置中即可),然后按照正常的python包方式调用
>2.客户端调用示例 

```
>> from msg_push import send_tasks
>> send_tasks.send_mail.delay({"RecvList":["example@example.com"],"Title":"Test","Content":"Test Mail"})
```
##扩展
>后续会添加 APP应用消息/短信 等处理

##部署
>采用虚拟环境进行部署+supervisor方式管理
>虚拟环境需要的依赖包,见git项目上 requirements.txt文件内容

##其他说明

##配置文件的使用/部署时的
配置文件见 msg_push/config.py
>1.其中包括了三个环境的配置信息描述,开发/测试/生产
>2.指定加载配置的地方见 msg_push/celery.py 中 f_app = create_app('default')
>

-------
2017-04-19 14:40:00
#增加简单的接口访问方式,提交请求.
接口部署方式
```push_svr_api.ini
[program:push_svr_api]
command=/{virtual_env}/bin/gunicorn -c /{code_path}/gunicorn.py wsgi:app
redirect_stderr=true
stdout_logfile=/tmp/push_svr_api.log
stdout_logfile_maxbytes=5MB
stdout_logfile_backups=10
directory=/{code_path}
user={user}
```
------
2017-04-27
#增加edm_mail信息处理批量的邮件/消息推送
部署方式
```edm_mail.ini
[program:edm_mail] 
command=/{virtualenv}/bin/celery -A edm_mail worker -n edmmail --loglevel=info 
redirect_stderr=true 
stdout_logfile=/tmp/oss_edm_mail.log 
stdout_logfile_maxbytes=1MB 
stdout_logfile_backups=10 
directory=/{code_path}/flask_proj 
user={user}
```
------
2017-06-15
#增加异常调用告警信息上报
部署方式
```monitor_alarm.ini
[program:monitor_alarm] 
command=/{virtualenv}/bin/celery -A monitor_alarm worker -n monitoralarm --loglevel=info 
redirect_stderr=true 
stdout_logfile=/tmp/oss_monitor_alarm.log 
stdout_logfile_maxbytes=1MB 
stdout_logfile_backups=10 
directory=/{code_path}/flask_proj 
user={user}
```
#采用gunicorn  gevent进行部署api时配置文件范例
guicorn.py
import os

bind='127.0.0.1:5000'
workers =4
backlog=2048
worker_class="gevent"
debug=True
proc_name="api.proc"
pidfile="/tmp/api.proc.pid"
logfile="/tmp/api.proc.log"
loglevel='debug'
```


