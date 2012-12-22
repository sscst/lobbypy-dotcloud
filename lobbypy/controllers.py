from sqlalchemy import and_, or_
from lobbypy.models import Lobby, Team, LobbyPlayer, spectator_table
from lobbypy.utils import db

def leave_or_delete_all_lobbies(player):
    old_lobbies = Lobby.query.\
        filter(or_(
            and_(
                Lobby.id == Team.lobby_id,
                LobbyPlayer.team_id == Team.id,
                LobbyPlayer.player_id == player.id,
            ), and_(
                Lobby.id == spectator_table.c.lobby_id,
                spectator_table.c.player_id == player.id,
                ))).all()
    for lobby in old_lobbies:
        if l.owner.id == player.id:
            db.session.remove(lobby)
            yield (lobby, True)
        else:
            lobby.leave(player)
            db.session.add(lobby)
            yield (lobby, False)
