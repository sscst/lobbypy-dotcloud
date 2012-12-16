import os
from socketio.server import SocketIOServer
from flask import Flask
from flask.ext.mako import MakoTemplates

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID

app = Flask(__name__)
app.secret_key = os.environ['SESSION_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DEV_DATABASE_URI']
app.debug = False
app.config['TESTING'] = False

mako = MakoTemplates(app)
db = SQLAlchemy(app)
oid = OpenID(app)
from lobbypy import views
from lobbypy import models
