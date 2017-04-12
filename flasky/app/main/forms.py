#!-*-encoding:utf8-*-
from flask.ext.wtf import FlaskForm as Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

class NameForm(Form):
    name = StringField('what is your name?',validators=[Required()])
    submit = SubmitField('Submit')
