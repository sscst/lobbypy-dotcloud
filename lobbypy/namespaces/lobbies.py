from flask import g, request
from json import dumps, loads, JSONEncoder
from lobbypy import db
from lobbypy.models import Lobby, Player
from .base import BaseNamespace, RedisListenerMixin

class LobbiesNamespace(BaseNamespace, RedisListenerMixin):
    def on_subscribe(self):
        """Subscribe to lobby CUD listener"""
        lobby_listing = [make_lobby_dict(l) for l in lobbies]
        self.spawn(self.listener, '/lobby/')
        return True, lobby_listing

    def on_get_lobby_listing(self):
        """Get full lobby listing"""
        lobbies = Lobby.query.all()
        lobby_listing = [make_lobby_dict(l) for l in lobbies]
        return True, lobby_listing

    def on_redis_update(self, lobby):
        self.emit('update', lobby)

    def on_redis_create(self, lobby):
        self.emit('create', lobby)

    def on_redis_delete(self, lobby_id):
        self.emit('delete', lobby_id)

def make_lobby_json(lobby):
    return dumps(lobby, cls=LobbiesNamespaceJSONEncoder)

def make_lobby_dict(l):
    return {
            'id': l.id,
            'name': l.name,
            'owner': make_player_dict(l.owner),
            'game_map': l.game_map,
            'players': l.player_count,
            'spectators': l.spectator_count,
            }

def make_player_dict(p):
    return {
            'id': p.id,
            'steam_id': p.steam_id,
            'name': p.name
            }

class LobbiesNamespaceJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Player):
            return make_player_dict(o)
        elif isinstance(o, Lobby):
            return make_lobby_dict(o)
        return JSONEncoder.default(self, o)
