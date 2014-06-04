import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, UPLOAD_FOLDER
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view ='login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
from app import views, models
