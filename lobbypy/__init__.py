import os
from flask import Flask
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

app = Flask(__name__)
app.secret_key = os.environ['SESSION_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ[
        'DATABASE_URI']
app.debug = True

db.init_app(app)
oid.init_app(app)

# Declare views
app.add_url_rule('/', view_func=index)
app.add_url_rule('/login', view_func=login)
app.add_url_rule('/logout', view_func=logout)

# Events
app.before_request(before_request)
