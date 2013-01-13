import os
from datetime import timedelta
from socketio.server import SocketIOServer
from flask import Flask
from lobbypy.utils import db, mako, oid, cache

def create_app():
    return Flask(__name__)

def config_app(app, **config):
    app.secret_key = (config.get('SESSION_KEY', None)
            or os.environ['SESSION_KEY'])
    app.config['SQLALCHEMY_DATABASE_URI'] = (
            config.get('SQLALCHEMY_DATABASE_URI', None)
            or os.environ['SQLALCHEMY_DATABASE_URI'])
    app.debug = config.get('DEBUG', False)
    app.config['TESTING'] = config.get('TESTING', False)
    app.config['RCON_CHECK_SERVER'] = config.get('RCON_CHECK_SERVER', True)
    app.config['CACHE_TYPE'] = config.get('CACHE_TYPE', 'null')
    if app.config['CACHE_TYPE'] == 'redis':
        app.config['CACHE_REDIS_HOST'] = config['CACHE_REDIS_HOST']
        app.config['CACHE_REDIS_PORT'] = config.get('CACHE_REDIS_PORT', None)
        app.config['CACHE_REDIS_PASSWORD'] = config.get('CACHE_REDIS_PASSWORD',
                None)
    ADMIN_URL = config.get('ADMIN_URL', 'admin')
    app.config['ADMIN_AUTH_TIMEOUT'] = config.get('ADMIN_AUTH_TIMEOUT',
            timedelta(hours=1))

    mako.init_app(app)
    db.init_app(app)
    cache.init_app(app)
    oid.init_app(app)
    from lobbypy import models
    from lobbypy import views

    app.add_url_rule('/', view_func=views.index)
    app.add_url_rule('/login', view_func=views.login)
    app.add_url_rule('/logout', view_func=views.logout)
    app.add_url_rule('/%s' % ADMIN_URL, view_func=views.admin, methods=['GET', 'POST'])
    app.add_url_rule('/socket.io/<path:path>', view_func=views.run_socketio)

    app.before_request(views.before_request)

    # ADMIN REST
    app.add_url_rule('/admin/rest/players',
        view_func=views.PlayerListingAPI.as_view('player_listing'))
    app.add_url_rule('/admin/rest/players/<int:player_id>',
        view_func=views.PlayerAPI.as_view('player'))
    app.add_url_rule('/admin/rest/lobbies',
        view_func=views.LobbyListingAPI.as_view('lobby_listing'))
    app.add_url_rule('/admin/rest/lobbies/<int:lobby_id>',
        view_func=views.LobbyAPI.as_view('lobby'))
    app.add_url_rule('/admin/rest/lobbies/<int:lobby_id>/teams',
        view_func=views.TeamListingAPI.as_view('team_listing'))
    app.add_url_rule(('/admin/rest/lobbies/<int:lobby_id>'
        '/teams/<int:team_id>'),
        view_func=views.TeamAPI.as_view('team'))
    app.add_url_rule(('/admin/rest/lobbies/<int:lobby_id>'
        '/spectators'),
        view_func=views.SpectatorListingAPI.as_view('spectator_listing'))
    app.add_url_rule(('/admin/rest/lobbies/<int:lobby_id>'
        '/spectators/<int:player_id>'),
        view_func=views.SpectatorAPI.as_view('spectator'))
    app.add_url_rule(('/admin/rest/lobbies/<int:lobby_id>'
        '/teams/<int:team_id>/players'),
        view_func=views.LobbyPlayerListingAPI.as_view('lobby_player_listing'))
    app.add_url_rule(('/admin/rest/lobbies/<int:lobby_id>'
        '/teams/<int:team_id>/players/<int:player_id>'),
        view_func=views.LobbyPlayerAPI.as_view('lobby_player'))
