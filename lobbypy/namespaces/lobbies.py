from flask import g, request
from json import dumps, loads, JSONEncoder
from lobbypy.utils import db
from lobbypy.models import Lobby, Player, make_lobby_item_dict
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
        lobby_listing = [make_lobby_item_dict(l) for l in lobbies]
        return True, lobby_listing

    def on_redis_update(self, lobby):
        self.emit('update', lobby)

    def on_redis_create(self, lobby):
        self.emit('create', lobby)

    def on_redis_delete(self, lobby_id):
        self.emit('delete', lobby_id)
