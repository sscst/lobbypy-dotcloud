from flask import g
from lobbypy.models import Lobby, make_lobby_item_dict, make_lobby_dict
from lobbypy.utils import db
from lobbypy.controllers import leave_or_delete_all_lobbies
from .base import BaseNamespace, RedisListenerMixin, RedisBroadcastMixin

class LobbyNamespace(BaseNamespace, RedisListenerMixin, RedisBroadcastMixin):
    def initialize(self):
        self.lobby_id = None
        self.listener_job = None

    def get_initial_acl(self):
        return set(['on_join', 'recv_connect'])

    def recv_connect(self):
        if g.player:
            self.add_acl_method('on_create_lobby')

    def disconnect(self, *args, **kwargs):
        """On disconnect leave lobby"""
        if g.player and self.lobby_id:
            lobby = Lobby.query.get(self.lobby_id)
            if lobby.owner is g.player:
                db.session.remove(lobby)
                db.session.commit()
                self.broadcast_event('/lobby/', 'delete', lobby_id)
                self.broadcast_event('/lobby/%d' % lobby_id, 'delete')
            else:
                lobby.leave(g.player)
                db.session.commit()
                self.broadcast_event('/lobby/', 'update',
                        make_lobby_item_dict(lobby))
                self.broadcast_event('/lobby/%d', 'update',
                        make_lobby_dict(lobby))
        super(LobbyNamespace, self).disconnect(*args, **kwargs)

    def on_redis_update(self, lobby_info):
        p_ids = [p[id] for p in lobby_info['spectators']]
        p_ids.extend([lp['player']['id'] for lp in [t['players'] for t in
            teams]])
        if not g.player or g.player.id in p_ids:
            self.emit('update', lobby_info)
        else:
            self.emit('leave')

    def on_redis_delete(self):
        self.emit('delete')

    def broadcast_leave_or_delete(self, lobby, is_delete):
        if is_delete:
            self.broadcast_event('/lobby/', 'delete', lobby.id)
            self.broadcast_event('/lobby/%d', 'delete', lobby.id)
        else:
            self.broadcast_event('/lobby/', 'update',
                    make_lobby_item_dict(lobby))
            self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))

    def on_create_lobby(self, name, server_info, game_map):
        """Create and join lobby"""
        assert g.player
        assert not self.lobby_id
        # Leave or delete old lobbies
        lobby_deletes = leave_or_delete_all_lobbies(g.player)
        # TODO: pull/generate password from list
        lobby = Lobby(name, g.player, server_info, game_map, 'password')
        lobby.join(g.player)
        db.session.add(lobby)
        db.session.commit()
        self.broadcast_event('/lobby/', 'create', make_lobby_item_dict(lobby))
        # Send leave or deletes
        [self.broadcast_leave_or_delete(*l_d) for l_d in lobby_deletes]
        self.add_acl_method('on_set_team')
        self.add_acl_method('on_leave')
        self.del_acl_method('on_create_lobby')
        self.del_acl_method('on_join')
        self.lobby_id = lobby.id
        self.listener_job = self.spawn(self.listener, '/lobby/%d' % lobby.id)
        return True, lobby.id

    def on_join(self, lobby_id):
        """Join lobby"""
        lobby = Lobby.query.get(lobby_id)
        if g.player:
            # Leave or delete old lobbies
            lobby_deletes = leave_or_delete_all_lobbies(g.player)
            lobby.join(g.player)
            db.session.commit()
            self.broadcast_event('/lobby/', 'update',
                    make_lobby_item_dict(lobby))
            self.broadcast_event('/lobby/%d' % lobby_id, 'update',
                    make_lobby_dict(lobby))
            # Send leave or deletes
            [self.broadcast_leave_or_delete(*l_d) for l_d in lobby_deletes]
            self.add_acl_method('on_set_team')
            self.del_acl_method('on_create_lobby')
            self.del_acl_method('on_join')
        self.add_acl_method('on_leave')
        self.lobby_id = lobby_id
        self.listener_job = self.spawn(self.listener, '/lobby/%d' % lobby_id)
        return True

    def on_leave(self):
        """Leave lobby"""
        assert self.lobby_id
        assert self.listener_job
        lobby = Lobby.query.get(self.lobby_id)
        if g.player:
            if lobby.owner is g.player:
                db.session.remove(lobby)
                db.session.commit()
                self.broadcast_event('/lobby/', 'delete', lobby_id)
                self.broadcast_event('/lobby/%d' % lobby_id, 'delete')
            else:
                lobby.leave(g.player)
                db.session.commit()
                self.broadcast_event('/lobby/', 'update',
                        make_lobby_item_dict(lobby))
                self.broadcast_event('/lobby/%d', 'update',
                        make_lobby_dict(lobby))
            self.del_acl_method('on_set_team')
            if 'on_set_class' in self.allowed_methods:
                self.del_acl_method('on_set_class')
                self.del_acl_method('on_toggle_ready')
            self.del_acl_method('on_leave')
            self.add_acl_method('on_join')
            self.add_acl_method('on_create_lobby')
        self.listener_job.kill()
        self.lobby_id = None
        return True

    def on_set_team(self, team_id):
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.set_team(g.player, team_id)
        db.session.commit()
        self.broadcast_event('/lobby/', 'update', make_lobby_item_dict(lobby))
        self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))
        if team_id is not None:
            self.add_acl_method('on_set_class')
            self.add_acl_method('on_toggle_ready')
        else:
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_toggle_ready')
        return True

    def on_set_class(self, class_id):
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.set_class(g.player, class_id)
        db.session.commit()
        self.broadcast_event('/lobby/', 'update', make_lobby_item_dict(lobby))
        self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))
        return True

    def on_toggle_ready(self):
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.toggle_ready(g.player)
        db.session.commit()
        self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))
        if lobby.is_ready_player(g.player):
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_set_team')
        else:
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_set_team')
        return True

    def on_start(self):
        pass
