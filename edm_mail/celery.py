#!-*-encoding:utf8-*-
from __future__ import absolute_import
import os
import sys
from celery import Celery
#from proj.flaskapp import create_app
from edm_mail import create_app
from flask_mail import Mail

#f_app = create_app(os.getenv('FLASK_SVR') or 'testing')
f_app = create_app('default')
mail = Mail(f_app)
mail.init_app(f_app)
f_app.app_context().push()

def make_celery(app):
    celery = Celery(app.import_name,include=['edm_mail.send_tasks'])
    celery.config_from_object('edm_mail.config')
    celery.conf.update(app.config)

    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract =True
        def __call__(self,*args,**kwargs):
            with app.app_context():
                return TaskBase.__call__(self,*args,**kwargs)
    celery.Task =ContextTask
    return celery

app = make_celery(f_app)

if __name__ == '__main__':
    app.start()