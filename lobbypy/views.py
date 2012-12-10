import re
from flask import (
        session,
        flash,
        redirect,
        g,
        )
from flask.ext.openid import OpenID

from lobbypy.models import db, Player

oid = OpenID()

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

def index():
    return 'Hello %s!' % session.get('user_id', 'Anonymous')

@oid.loginhandler
def login():
    if g.player is not None:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):
    match = _steam_id_re.search(resp.identity_url)
    g.player = Player.get_or_create(match.group(1))
    db.session.commit()
    session['user_id'] = g.player.id
    flash('You are logged in as %s' % g.player.steam_id)
    return redirect(oid.get_next_url())

def before_request():
    g.player = None
    if 'user_id' in session:
        g.player = Player.query.get(session['user_id'])

def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())

