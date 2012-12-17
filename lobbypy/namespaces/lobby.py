from .base import BaseNamespace

class LobbyNamespace(BaseNamespace):
    def initialize(self):
        self.lobby_id = None

    def listener(self):
        pass

    def on_create_lobby(self, name, server_info, game_map):
        """Create lobby"""
        # TODO: pull/generate password from list
        lobby = Lobby(name, g.player, server_info, game_map, 'password')
        db.session.add(lobby)
        db.session.commit()
        return True, lobby.id

    def on_join(self, lobby_id):
        # Leave the old lobby if we have not
        if self.lobby_id is not None:
            self.on_leave()
        lobby = Lobby.query.get(lobby_id)
        lobby.join(player)
        db.session.commit()
        self.lobby_id = lobby_id
        return True

    def on_leave(self):
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        if lobby.owner is g.player:
            db.session.remove(lobby)
        else:
            lobby.leave(player)
        db.session.commit()
        self.lobby_id = None
        return True

    def on_set_team(self, team_id):
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        lobby.set_team(g.player, team_id)
        db.session.commit()
        return True

    def on_set_class(self, class_id):
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        lobby.set_class(g.player, class_id)
        db.session.commit()
        return True

    def on_toggle_ready(self):
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        lobby.toggle_ready(player)
        db.session.commit()
        return True

    def on_start(self):
        pass
