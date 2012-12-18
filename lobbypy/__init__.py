import os
from socketio.server import SocketIOServer
from flask import Flask
from flask.ext.mako import MakoTemplates

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID

app = Flask(__name__)
mako = MakoTemplates()
db = SQLAlchemy()
oid = OpenID()
def config_app(**config):
    app.secret_key = (config.get('SESSION_KEY', None)
            or os.environ['SESSION_KEY'])
    app.config['SQLALCHEMY_DATABASE_URI'] = (
            config.get('DEV_DATABASE_URI', None)
            or os.environ['DEV_DATABASE_URI'])
    app.debug = config.get('DEBUG', None) or False
    app.config['TESTING'] = config.get('TESTING', None) or False

    mako.init_app(app)
    db.init_app(app)
    oid.init_app(app)
    from lobbypy import views
    from lobbypy import models
