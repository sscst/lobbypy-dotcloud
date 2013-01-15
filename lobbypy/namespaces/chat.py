import re
from flask import g, current_app
from lobbypy.models import Player, make_player_dict
from .base import BaseNamespace, RedisListenerMixin, RedisBroadcastMixin

channel_pattern = re.compile('/chat/(?P<type>\w+)/(?P<dest>\w+)')
class ChatNamespace(BaseNamespace, RedisListenerMixin, RedisBroadcastMixin):
    def get_initial_acl(self):
        return set(['on_join', 'on_part', 'recv_connect'])

    def get_channel_name(self, channel):
        return '/chat/%s/%s' % (channel['type'], channel['dest'])

    def get_channel_from_name(self, name):
        m = channel_pattern.match(name)
        if not m:
            raise ValueError
        return {'type':m.group('type'), 'dest':m.group('dest')}

    def recv_connect(self):
        if g.player:
            self.add_acl_method('on_send')

    def on_join(self, channel):
        if self.subscribe_allowed(channel):
            current_app.logger.info('Player: %s joined channel: %s' % (
                g.player.id if g.player else 'Anonymous', channel))
            self.subscribe(self.get_channel_name(channel))
            return True
        return False

    def on_part(self, channel):
        if 'type' not in channel or 'dest' not in channel:
            return False
        self.unsubscribe(self.get_channel_name(channel))
        return True

    def on_send(self, channel, data):
        if self.get_channel_name(channel) not in self.pubsub.channels:
            return False
        if not self.publish_allowed(channel):
            return False
        if self.verify(data):
            current_app.logger.info('Player %s sent: %s to channel: %s' % (
                g.player.id if g.player else 'Anonymous', data, channel))
            self.broadcast_event(self.get_channel_name(channel), 'send',
                    g.player.id, data)
            return True
        return False

    def on_redis_send(self, channel_name, sender_id, data):
        player = Player.query.get(sender_id)
        assert player
        channel = self.get_channel_from_name(channel_name)
        self.emit('message', channel, make_player_dict(player), data)

    def subscribe_allowed(self, channel):
        if 'type' not in channel or 'dest' not in channel:
            return False
        if channel['type'] == 'channel':
            name = channel['dest']
            return name == 'root'
        if channel['type'] == 'player':
            p_id = channel['dest']
            player = Player.query.get(p_id)
            if player:
                return player == g.player
            return False
        if channel['type'] == 'lobby':
            l_id = channel['dest']
            lobby = Lobby.query.get(l_id)
            return lobby is not None
        return False

    def publish_allowed(self, channel):
        if 'type' not in channel or 'dest' not in channel:
            return False
        if not g.player:
            return False
        if channel['type'] == 'channel':
            name = channel['dest']
            return name == 'root'
        if channel['type'] == 'player':
            p_id = channel['dest']
            player = Player.query.get(p_id)
            return player is not None
        if channel['type'] == 'lobby':
            l_id = channel['dest']
            lobby = Lobby.query.get(l_id)
            if lobby:
                return g.player in lobby
            return False
        return False

    def verify(self, data):
        return isinstance(data, basestring)
