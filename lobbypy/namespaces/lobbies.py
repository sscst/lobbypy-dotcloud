import redis
from flask import g, request
from json import dumps, loads, JSONEncoder
from socketio.namespace import BaseNamespace
from lobbypy import app, db

class LobbiesNamespace(BaseNamespace):
    def initialize(self):
        request = self.request
        self.ctx = app.request_context(request.environ)
        self.ctx.push()
        app.preprocess_request()
        del self.request

    def disconnect(self, *args, **kwargs):
        super(LobbiesNamespace, self).disconnect(self, *args, **kwargs)
        self.ctx.pop()

    def listener(self):
        r = redis.StrictRedis()
        r = r.pubsub()

        r.subscribe('lobbies')

        for m in r.listen():
            if m['type'] == 'message':
                data = loads(m['data'])
                if data['type'] == 'update':
                    self.emit('update', data['lobby'])
                elif data['type'] == 'destroy':
                    self.emit('destroy', data['lobby_id'])
                elif data['type'] == 'create':
                    self.emit('create', data['lobby'])

    def on_subscribe(self):
        self.on_get_lobby_listing()
        self.spawn(self.listener)
        return True

    def on_get_lobby_listing(self):
        from lobbypy.models import Lobby
        lobbies = Lobby.query.all()
        lobby_listing = [make_lobby_json(l) for l in lobbies]
        self.emit('lobby_listing', lobby_listing)
        return True, lobby_listing

    def on_create_lobby(self, name, server_info, game_map):
        print g._get_current_object()
        from lobbypy.models import Lobby
        # TODO: pull/generate password from list
        lobby = Lobby(name, g.player, server_info, game_map, None)
        db.session.add(lobby)
        db.session.commit()
        print lobby
        return True, lobby.id

def make_lobby_json(lobby):
    return dumps(lobby, cls=LobbiesNamespaceJSONEncoder)

class LobbiesNamespaceJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Player):
            return {
                    'id': o.id,
                    'steam_id': o.steam_id,
                    'name': o.name
                    }
        elif isinstance(o, Lobby):
            return {
                    'id': o.id,
                    'name': o.name,
                    'owner': o.owner,
                    'game_map': o.game_map,
                    'players': o.player_count,
                    'spectators': o.spectator_count,
                    }
        return JSONEncoder.default(self, o)
