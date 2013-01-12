from flask import g, request, current_app
from json import dumps, loads, JSONEncoder
from lobbypy.utils import db
from lobbypy.models import Lobby, Player, make_lobby_item_dict
from .base import BaseNamespace, RedisListenerMixin

class LobbiesNamespace(BaseNamespace, RedisListenerMixin):
    def on_subscribe(self):
        """Subscribe to lobby CUD listener"""
        lobby_listing = [make_lobby_dict(l) for l in Lobby.query.all()]
        self.subscribe('/lobby/')
        current_app.logger.info('Player: %s subscribed to LobbiesNamespace' %
                g.player.id if g.player else 'Anonymous')
        return True, lobby_listing

    def on_unsubscribe(self):
        self.unsubscribe('/lobby/')

    def on_get_lobby_listing(self):
        """Get full lobby listing"""
        lobbies = Lobby.query.all()
        lobby_listing = [make_lobby_item_dict(l) for l in lobbies]
        current_app.logger.info('Player: %s got lobby listing to LobbiesNamespace' %
                g.player.id if g.player else 'Anonymous')
        return True, lobby_listing

    def on_redis_update(self, channel, lobby_info):
        self.emit('update', lobby_info)
        current_app.logger.debug(
                'Emitting update with %s to Player %s on Socket %s' %
                (lobby_info, g.player.id if g.player else
                'Anonymous', 'None'))

    def on_redis_create(self, channel, lobby_info):
        self.emit('create', lobby_info)
        current_app.logger.debug(
                'Emitting create with %s to Player %s on Socket %s' %
                (lobby_info, g.player.id if g.player else
                'Anonymous', 'None'))

    def on_redis_delete(self, channel, lobby_id):
        self.emit('delete', lobby_id)
        current_app.logger.debug(
                'Emitting delete with %d to Player %s on Socket %s' %
                (lobby_id, g.player.id if g.player else
                'Anonymous', 'None'))
