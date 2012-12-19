from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.mako import MakoTemplates

mako = MakoTemplates()
db = SQLAlchemy()
oid = OpenID()
