import os
import sys
from flask import Flask
#from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

app = Flask(__name__)
app.config.from_object('config')
#bootstrap = Bootstrap()
lm = LoginManager()
lm.login_view = 'login'
#oid = OpenID(app, os.path.join(basedir, 'tmp'))
db = SQLAlchemy()

def create_app(config_name):
    
    

    #bootstrap.init_app(app)
    
    db.init_app(app)
    lm.init_app(app)
    
    
    import views, models
    return app

