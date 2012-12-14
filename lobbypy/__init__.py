import os
from flask import Flask
from flask.ext.mako import MakoTemplates
from lobbypy.views import (
        oid,
        # VIEW FUNCTIONS
        index,
        login,
        logout,
        # EVENTS
        before_request,
        )
from lobbypy.models import db

def create_app(**config):
    app = Flask(__name__)
    app.secret_key = config.get('SESSION_KEY', os.environ['SESSION_KEY'])
    app.config['SQLALCHEMY_DATABASE_URI'] = config.get(
            'SQLALCHEMY_DATABASE_URI',
            os.environ['DEV_DATABASE_URI'])
    app.debug = config.get('DEBUG', False)
    app.config['TESTING'] = config.get('TESTING', False)

    mako = MakoTemplates(app)

    db.init_app(app)
    oid.init_app(app)

    # Declare views
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/login', view_func=login)
    app.add_url_rule('/logout', view_func=logout)

    # Events
    app.before_request(before_request)

    return app
