from sqlalchemy import and_, or_
from flask import current_app
from lobbypy.models import Lobby, Team, LobbyPlayer, spectator_table
from lobbypy.utils import db

def leave_or_delete_all_lobbies(player):
    old_lobbies = Lobby.query.outerjoin(Team, LobbyPlayer, spectator_table).\
            filter(or_(LobbyPlayer.player_id == player.id,
                    spectator_table.c.player_id == player.id,
                Lobby.owner_id == player.id)).all()
    lobby_dels = []
    for lobby in old_lobbies:
        if lobby.owner.id == player.id:
            db.session.delete(lobby)
            lobby_dels.append((lobby, True))
            current_app.logger.info('Player: %d destroyed Lobby: %d' %
                    (player.id, lobby.id))
        else:
            lobby.leave(player)
            db.session.add(lobby)
            lobby_dels.append((lobby, False))
            current_app.logger.info('Player: %d left Lobby: %d' %
                    (player.id, lobby.id))
    return lobby_dels
