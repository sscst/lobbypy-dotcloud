from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.openid import OpenID
from flask.ext.mako import MakoTemplates
from flask.ext.cache import Cache

mako = MakoTemplates()
db = SQLAlchemy()
oid = OpenID()
cache = Cache()
