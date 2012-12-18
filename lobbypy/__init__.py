import os
from socketio.server import SocketIOServer
from flask import Flask
from lobbypy.utils import db, mako, oid

def create_app():
    return Flask(__name__)

def config_app(app, **config):
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
    from lobbypy import models
    from lobbypy import views

    app.add_url_rule('/', view_func=views.index)
    app.add_url_rule('/login', view_func=views.login)
    app.add_url_rule('/logout', view_func=views.logout)
    app.add_url_rule('/socket.io/<path:path>', view_func=views.run_socketio)
    app.before_request(views.before_request)
