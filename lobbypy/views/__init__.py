import re
from pbkdf2 import crypt
from socketio import socketio_manage
from flask import (
        session,
        request,
        Response,
        flash,
        redirect,
        g,
        current_app,
        url_for
        )
from flask.ext.mako import render_template
from lobbypy.utils import oid, db
from lobbypy.models import Player
from .utils import admin_check
from .rest import (
        PlayerAPI,
        PlayerListingAPI,
        LobbyAPI,
        LobbyListingAPI,
        SpectatorAPI,
        SpectatorListingAPI,
        TeamAPI,
        TeamListingAPI,
        LobbyPlayerAPI,
        LobbyPlayerListingAPI,
)

__all__ = ['index', 'login', 'logout', 'admin', 'PlayerAPI', 'LobbyAPI',
        'SpectatorAPI', 'TeamAPI', 'LobbyPlayerAPI', 'before_request',
        'LobbyListingAPI', 'PlayerListingAPI', 'SpectatorListingAPI',
        'TeamListingAPI', 'LobbyPlayerListingAPI']
_steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')

def index():
    hellouser = 'Hello %s!' % (g.player.name if g.player else 'Anonymous')
    return render_template('index.mako', **{
        'section': 'home',
        'hellouser': hellouser
    })

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
    session['username'] = g.player.name
    flash('You are logged in as %s' % g.player.steam_id)
    current_app.logger.info('Player %d logged in' % g.player.id)
    return redirect(oid.get_next_url())

def before_request():
    g.player = None
    g.admin_authed = False
    if 'user_id' in session:
        g.player = Player.query.get(session['user_id'])
    if 'auth_time' in session:
        # check timeout
        if (datetime.now() - session['auth_time'] >
                current_app.config['ADMIN_AUTH_TIMEOUT']):
            del session['auth_time']
        else:
            g.admin_authed = True

def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('auth_time', None)
    current_app.logger.info('Player %d logged out' % g.player.id)
    return redirect(oid.get_next_url())

@admin_check
def admin():
    if request.method == 'POST':
        hashed_pw = crypt(request.form['password'], g.player.password)
        if hashed_pw != g.player.password:
            g.player.auth_attempts += 1
            db.session.commit()
            if (g.player.auth_attempts >
                    current_app.config['MAX_AUTH_ATTEMPTS']):
                return render_template('admin_locked.mako')
            return render_template('admin_login.mako', **{
                'bad_pass': True
            })
        session['auth_time'] = datetime.now()
        redirect(url_for('admin'))
    if not g.admin_authed:
        # this admin has yet to log in
        return render_template('admin_login.mako')
    # we're golden like jarate
    return render_template('admin.mako')

def run_socketio(path):
    from lobbypy.namespaces import LobbiesNamespace, LobbyNamespace
    real_request = request._get_current_object()
    socketio_manage(request.environ, {
            '/lobbies': LobbiesNamespace,
            '/lobby': LobbyNamespace,
        },
        request=real_request)
    return Response()
