from flask import g, current_app
from srcdspy.rcon import RconException
from lobbypy.models import Lobby, Player, make_lobby_item_dict, make_lobby_dict
from lobbypy.utils import db
from lobbypy.controllers import leave_or_delete_all_lobbies
from lobbypy.lib.srcds_api import connect_rcon, connect_query, check_map, check_players
from .base import BaseNamespace, RedisListenerMixin, RedisBroadcastMixin

class LobbyNamespace(BaseNamespace, RedisListenerMixin, RedisBroadcastMixin):
    def initialize(self):
        self.lobby_id = None
        self.spawn(self.listener)

    def get_initial_acl(self):
        return set(['on_join', 'recv_connect'])

    def recv_connect(self):
        # Add create if we're authenticated
        if g.player:
            self.add_acl_method('on_create_lobby')
        current_app.logger.info('Player: %s connected to LobbyNamespace' %
                g.player.id if g.player else 'Anonymous')

    def disconnect(self, *args, **kwargs):
        """Disconnect handling"""
        # If auth'd and in a lobby, leave the lobby
        if g.player and self.lobby_id:
            lobby = Lobby.query.get(self.lobby_id)
            # If owner, this means delete, otherwise just leave
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
        current_app.logger.info('Player: %s disconnected from LobbyNamespace' %
                g.player.id if g.player else 'Anonymous')
        # Do real disconnect logic
        super(LobbyNamespace, self).disconnect(*args, **kwargs)

    def on_redis_update(self, channel, lobby_info):
        """Send update to user"""
        # Get full list of player ids
        p_ids = [p[id] for p in lobby_info['spectators']]
        p_ids.extend([lp['player']['id'] for lp in [t['players'] for t in
            teams]])
        # If we're in the lobby send the update, otherwise we left the lobby
        # elsewhere
        if not g.player or g.player.id in p_ids:
            self.emit('update', lobby_info)
            current_app.logger.debug('Emitting update with %s to Player: %s on Socket: %s',
                    (lobby_info, g.player.id if g.player else 'Anonymous', 'None'))
        else:
            self.emit('leave')
            current_app.logger.debug('Emitting leave to Player: %d on Socket: %s',
                    (g.player.id, 'None'))

    def on_redis_delete(self, channel):
        """Send delete to user"""
        self.emit('delete')
        current_app.logger.debug('Emitting delete to Player: %s on Socket: %s',
                (g.player.id if g.player else 'Anonymous', 'None'))

    def broadcast_leave_or_delete(self, lobby, is_delete):
        """Broadcast leave or delete to redis"""
        if is_delete:
            self.broadcast_event('/lobby/', 'delete', lobby.id)
            self.broadcast_event('/lobby/%d', 'delete', lobby.id)
        else:
            self.broadcast_event('/lobby/', 'update',
                    make_lobby_item_dict(lobby))
            self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))

    # ANON ALLOWED METHODS
    def on_join(self, lobby_id):
        """Join lobby"""
        lobby = Lobby.query.get(lobby_id)
        if g.player:
            # Leave or delete old lobbies
            lobby_deletes = leave_or_delete_all_lobbies(g.player)
            lobby.join(g.player)
            db.session.commit()
            # Broadcast update to the joined lobby and lobby listing
            self.broadcast_event('/lobby/', 'update',
                    make_lobby_item_dict(lobby))
            self.broadcast_event('/lobby/%d' % lobby_id, 'update',
                    make_lobby_dict(lobby))
            # Send leave or deletes
            [self.broadcast_leave_or_delete(*l_d) for l_d in lobby_deletes]
            # Update ACL
            self.add_acl_method('on_set_team')
            self.del_acl_method('on_create_lobby')
            self.del_acl_method('on_join')
            if lobby.owner == g.player:
                self.add_acl_method('on_kick')
                self.add_acl_method('on_set_lobby_name')
                self.add_acl_method('on_set_team_name')
        self.add_acl_method('on_leave')
        # Set lobby id and start listening on redis
        self.lobby_id = lobby_id
        self.subscribe('/lobby/%d' % lobby_id)
        current_app.logger.info('Player %s joined Lobby %d', (g.player.id if
            g.player else 'Anonymous', lobby_id))
        return True, make_lobby_dict(lobby)

    def on_leave(self):
        """Leave lobby"""
        assert self.lobby_id
        assert self.listener_job
        lobby = Lobby.query.get(self.lobby_id)
        # If we're auth'd do actual leave, otherwise just kill job and lobby_id
        if g.player:
            # If we're owner delete, if not just leave
            if lobby.owner is g.player:
                db.session.remove(lobby)
                db.session.commit()
                # Broadcast delete to lobby and lobby listing
                self.broadcast_event('/lobby/', 'delete', self.lobby_id)
                self.broadcast_event('/lobby/%d' % self.lobby_id, 'delete')
            else:
                lobby.leave(g.player)
                db.session.commit()
                # Broadcast leave to lobby and lobby listing
                self.broadcast_event('/lobby/', 'update',
                        make_lobby_item_dict(lobby))
                self.broadcast_event('/lobby/%d', 'update',
                        make_lobby_dict(lobby))
            # Update ACL
            self.del_acl_method('on_set_team')
            if 'on_set_class' in self.allowed_methods:
                self.del_acl_method('on_set_class')
                self.del_acl_method('on_toggle_ready')
            self.del_acl_method('on_leave')
            self.add_acl_method('on_join')
            self.add_acl_method('on_create_lobby')
        self.unsubscribe('/lobby/%d' % self.lobby_id)
        current_app.logger.info('Player %s left Lobby %d', (g.player.id if
            g.player else 'Anonymous', self.lobby_id))
        self.lobby_id = None
        return True

    # PLAYER ONLY METHODS
    def on_create_lobby(self, name, server_address, rcon_password, game_map):
        """Create and join lobby"""
        assert g.player
        assert not self.lobby_id
        # Check server
        if current_app.config.get('RCON_CHECK_SERVER', True):
            try:
                sr = connect_rcon(server_address, rcon_password)
                sq = connect_query(server_address)
            except RconException:
                return False, 'bad_pass'
            except Exception:
                return False, 'server_issue'
            else:
                if not check_map(sr):
                    return False, 'map_dne'
                # TODO: ask if you want to kick players
                if not check_players(sq):
                    return False, 'players'
                sr.close()
                sq.close()
        # Leave or delete old lobbies
        lobby_deletes = leave_or_delete_all_lobbies(g.player)
        # TODO: pull/generate password from list
        lobby = Lobby(name, g.player, server_address, rcon_password, game_map, 'password')
        lobby.join(g.player)
        db.session.add(lobby)
        db.session.commit()
        # Send event to redis
        self.broadcast_event('/lobby/', 'create', make_lobby_item_dict(lobby))
        # Send leave or deletes
        [self.broadcast_leave_or_delete(*l_d) for l_d in lobby_deletes]
        # Update ACL
        self.add_acl_method('on_set_team')
        self.add_acl_method('on_leave')
        self.del_acl_method('on_create_lobby')
        self.del_acl_method('on_join')
        self.add_acl_method('on_kick')
        self.add_acl_method('on_set_lobby_name')
        self.add_acl_method('on_set_team_name')
        # Set lobby id and start listening on redis
        self.lobby_id = lobby.id
        self.subscribe('/lobby/%d' % lobby.id)
        current_app.logger.info('Player %d created Lobby %d' % (g.player.id,
            lobby.id))
        return True, lobby.id

    def on_set_team(self, team_id):
        """Set team in lobby"""
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.set_team(g.player, team_id)
        db.session.commit()
        # Broadcast redis update
        self.broadcast_event('/lobby/', 'update', make_lobby_item_dict(lobby))
        self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))
        # Update ACL
        if team_id is not None:
            self.add_acl_method('on_set_class')
            self.add_acl_method('on_toggle_ready')
        else:
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_toggle_ready')
        current_app.logger.info('Player %d set team to %s', (g.player.id,
            team_id if team_id else 'Spectator'))
        return True

    def on_set_class(self, class_id):
        """Set class in lobby"""
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.set_class(g.player, class_id)
        db.session.commit()
        # Broadcast redis update
        self.broadcast_event('/lobby/', 'update', make_lobby_item_dict(lobby))
        self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))
        current_app.logger.info('Player %d set class to %s', (g.player.id,
            class_id if class_id else 'Random'))
        return True

    def on_toggle_ready(self):
        """Toggle ready in lobby"""
        assert self.lobby_id
        assert g.player
        lobby = Lobby.query.get(self.lobby_id)
        lobby.toggle_ready(g.player)
        db.session.commit()
        # Broadcast redis update
        self.broadcast_event('/lobby/%d', 'update', make_lobby_dict(lobby))
        # Update ACL
        if lobby.is_ready_player(g.player):
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_set_team')
        else:
            self.del_acl_method('on_set_class')
            self.del_acl_method('on_set_team')
        current_app.logger.info('Player %d toggled ready to %s', (g.player.id,
            lobby.is_ready_player(g.player)))
        return True

    # OWNER ONLY METHODS
    def on_start(self):
        pass

    def on_kick(self, player_id):
        """Kick a player from the lobby"""
        assert g.player
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        assert lobby.owner == g.player
        player = Player.query.get(player_id)
        if player is None:
            return False, 'player_dne'
        if not lobby.has_player(player):
            return False, 'player_dne_lobby'
        lobby.leave(player)
        db.session.commit()
        self.broadcast_event('/lobby/', 'update',
                make_lobby_item_dict(lobby))
        self.broadcast_event('/lobby/%d', 'update',
                make_lobby_dict(lobby))
        return True

    def on_ban(self, player_id):
        pass

    def on_set_team_name(self, team_id, name):
        assert g.player
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        assert lobby.owner == g.player
        if team_id is None:
            return False, 'team_is_spectator'
        if not team_id < len(lobby.teams):
            return False, 'team_dne'
        if name is None or len(name) == 0:
            return False, 'name_none'
        team = lobby.teams[team_id]
        team.name = name
        db.session.commit()
        self.broadcast_event('/lobby/%d', 'update',
                make_lobby_dict(lobby))
        return True

    def on_set_lobby_name(self, name):
        assert g.player
        assert self.lobby_id
        lobby = Lobby.query.get(self.lobby_id)
        assert lobby.owner == g.player
        if name is None or len(name) == 0:
            return False, 'name_none'
        lobby.name = name
        db.session.commit()
        self.broadcast_event('/lobby/', 'update',
                make_lobby_item_dict(lobby))
        self.broadcast_event('/lobby/%d', 'update',
                make_lobby_dict(lobby))

    def on_give_owner(self):
        pass
