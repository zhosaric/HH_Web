from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SubmitField
from wtforms.validators import Required, Length
from flask.ext.wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(Form):
	openid = TextField('openid', validators = [Required()])
	remember_me = BooleanField('remember_me', default = False)

class HistoryForm(Form):
	fileName = FileField('hfile', validators =[FileRequired(), FileAllowed(['txt'], 'Text Files Only!')])
	submit = SubmitField("Submit")