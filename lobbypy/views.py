import re
from flask import (
        session,
        request,
        Response,
        flash,
        redirect,
        g,
        )
from flask.ext.mako import render_template
from lobbypy import app, oid, db

from socketio import socketio_manage

_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

@app.route('/')
def index():
    hellouser = 'Hello %s!' % session.get('user_id', 'Anonymous')
    return render_template('index.mako', **{
        'section': 'home',
        'hellouser': hellouser
    })

@app.route('/login')
@oid.loginhandler
def login():
    if g.player is not None:
        return redirect(oid.get_next_url())
    return oid.try_login('http://steamcommunity.com/openid')

@oid.after_login
def create_or_login(resp):
    from lobbypy.models import Player
    match = _steam_id_re.search(resp.identity_url)
    g.player = Player.get_or_create(match.group(1))
    session['user_id'] = g.player.id
    flash('You are logged in as %s' % g.player.steam_id)
    return redirect(oid.get_next_url())

@app.before_request
def before_request():
    from lobbypy.models import Player
    g.player = None
    if 'user_id' in session:
        g.player = Player.query.get(session['user_id'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(oid.get_next_url())

@app.route('/socket.io/<path:path>')
def run_socketio(path):
    from lobbypy.namespaces import LobbiesNamespace, LobbyNamespace
    real_request = request._get_current_object()
    socketio_manage(request.environ, {
            '/lobbies': LobbiesNamespace,
            '/lobby': LobbyNamespace,
        },
        request=real_request)
    return Response()
