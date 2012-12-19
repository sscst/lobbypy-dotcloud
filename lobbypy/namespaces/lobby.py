from flask import g
from lobbypy import db
from lobbypy.models import Lobby
from .base import BaseNamespace

class LobbyNamespace(BaseNamespace):
    def initialize(self):
        self.lobby_id = None
        self.listener_job = None

    def get_initial_acl(self):
        return set(['on_join', 'recv_connect'])

    def listener(self):
        pass

    def recv_connect(self):
        if g.player:
            self.add_acl_method('on_create_lobby')

    def on_create_lobby(self, name, server_info, game_map):
        """Create lobby"""
        # TODO: pull/generate password from list
        lobby = Lobby(name, g.player, server_info, game_map, 'password')
        db.session.add(lobby)
        db.session.commit()
        return True, lobby.id

    def on_join(self, lobby_id):
        # Leave the old lobby if we have not
        lobby = Lobby.query.get(lobby_id)
        if g.player:
            if self.lobby_id is not None:
                self.on_leave()
            lobby.join(g.player)
            db.session.commit()
            self.add_acl_method('on_set_team')
            self.del_acl_method('on_create_lobby')
            self.del_acl_method('on_join')
        self.add_acl_method('on_leave')
        self.lobby_id = lobby_id
        self.listener_job = self.spawn(self.listener)
        return True

    def on_leave(self):
        assert self.lobby_id
        assert self.listener
        lobby = Lobby.query.get(self.lobby_id)
        if g.player:
            if lobby.owner is g.player:
                db.session.remove(lobby)
            else:
                lobby.leave(g.player)
            db.session.commit()
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
        return True

    def on_toggle_ready(self):
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.toggle_ready(g.player)
        db.session.commit()
        if lobby.is_ready_player(g.player):
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_set_team')
        else:
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_set_team')
        return True

    def on_start(self):
        pass
