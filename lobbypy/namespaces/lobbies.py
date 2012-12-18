import redis
from flask import g, request
from json import dumps, loads, JSONEncoder
from lobbypy import db
from lobbypy.models import Lobby, Player
from .base import BaseNamespace

class LobbiesNamespace(BaseNamespace):
    def listener(self):
        """Listen on redis for lobby CUD"""
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
        """Subscribe to lobby CUD listener"""
        self.on_get_lobby_listing()
        self.spawn(self.listener)
        return True

    def on_get_lobby_listing(self):
        """Get full lobby listing"""
        lobbies = Lobby.query.all()
        lobby_listing = [make_lobby_json(l) for l in lobbies]
        return True, lobby_listing

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
