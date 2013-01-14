from flask import request, abort
from flask.views import MethodView

from lobbypy.models import Player, Lobby, Team, LobbyPlayer
from lobbypy.models.utils import (
        make_player_dict,
        make_lobby_dict,
        make_team_dict,
        make_lobby_player_dict
        )
from lobbypy.utils import db
from .utils import admin_check, jsonify

class PlayerListingAPI(MethodView):
    def get(self):
        players = Player.query.all()
        player_dicts = [make_player_dict(p) for p in players]
        return jsonify(200, players = player_dicts)

    @admin_check
    def post(self):
        p = Player(request.form['steam_id'])
        db.session.add(p)
        db.session.commit()
        return jsonify(201, id=p.id)

class PlayerAPI(MethodView):
    def get(self, player_id):
        player = Player.query.get_or_404(player_id)
        return jsonify(200, player = make_player_dict(player))

    @admin_check
    def put(self, player_id):
        p = Player.query.get(player_id)
        if not p:
            abort(404)
        if 'steam_id' in request.form:
            p.steam_id = request.form['steam_id']
        db.session.commit()
        return jsonify(200)

    @admin_check
    def delete(self, player_id):
        p = Player.query.get(player_id)
        if not p:
            abort(404)
        db.session.delete(p)
        db.session.commit()
        return jsonify(200)

class LobbyListingAPI(MethodView):
    def get(self):
        lobbies = Lobby.query.all()
        lobby_dicts = [make_lobby_dict(l) for l in lobbies]
        return jsonify(200, lobbies = lobby_dicts)

    @admin_check
    def post(self):
        o_id = request.form['owner_id']
        name = request.form['name']
        server_address = request.form['server_address']
        rcon_password = request.form['rcon_password']
        game_map = request.form['game_map']
        password = request.form['password']
        o = Player.query.get(o_id)
        if not o:
            abort(405)
        l = Lobby(name, o, server_address, rcon_password, game_map, password)
        db.session.add(l)
        db.session.commit()
        return jsonify(201, id=l.id)

class LobbyAPI(MethodView):
    def get(self, lobby_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        return jsonify(200, lobby = make_lobby_dict(lobby))

    @admin_check
    def put(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if 'owner_id' in request.form:
            o = Player.query.get(request.form['owner_id'])
            if not o:
                abort(405)
            l.owner = o
        if 'name' in request.form:
            l.name = request.form['name']
        if 'server_address' in request.form:
            l.server_address = request.form['server_address']
        if 'rcon_password' in request.form:
            l.rcon_password = request.form['rcon_password']
        if 'game_map' in request.form:
            l.game_map = request.form['game_map']
        db.session.commit()
        print 'committed'
        return jsonify(200)

    @admin_check
    def delete(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        db.session.delete(l)
        db.session.commit()
        return jsonify(200)

class SpectatorListingAPI(MethodView):
    def get(self, lobby_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        player_dicts = [make_player_dict(p) for p in lobby.spectators]
        return jsonify(200, spectators = player_dicts)

    @admin_check
    def post(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if 'player_id' not in request.form:
            abort(405)
        p_id = request.form['player_id']
        p = Player.query.get(p_id)
        if not p:
            abort(405)
        l.spectators.append(p)
        db.session.commit()
        return jsonify(200)

class SpectatorAPI(MethodView):
    def get(self, lobby_id, player_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        player = Player.query.get_or_404(player_id)
        if player not in lobby.spectators:
            abort(404)
        return jsonify(200, spectator = make_player_dict(player))

    @admin_check
    def delete(self, lobby_id, player_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        p = Player.query.get(player_id)
        if not p:
            abort(405)
        l.spectators.remove(p)
        db.session.commit()
        return jsonify(200)

class TeamListingAPI(MethodView):
    def get(self, lobby_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        team_dicts = [make_team_dict(i, t) for i, t in enumerate(lobby.teams)]
        return jsonify(200, teams = team_dicts)

    @admin_check
    def post(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if 'name' not in request.form:
            abort(405)
        t = Team(request.form['name'])
        l.teams.append(t)
        db.session.commit()
        return jsonify(201, id=len(l.teams) - 1)

class TeamAPI(MethodView):
    def get(self, lobby_id, team_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        if team_id >= len(lobby.teams) or team_id < 0:
            abort(404)
        return jsonify(200, team = make_team_dict(team_id, lobby.teams[team_id]))

    @admin_check
    def put(self, lobby_id, team_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        if 'name' in request.form:
            t.name = request.form['name']
        db.session.commit()
        return jsonify(200)

    @admin_check
    def delete(self, lobby_id, team_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        db.session.delete(t)
        db.session.commit()
        return jsonify(200)

class LobbyPlayerListingAPI(MethodView):
    def get(self, lobby_id, team_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        if team_id >= len(lobby.teams) or team_id < 0:
            abort(404)
        players_dict = [make_lobby_player_dict(lp) for lp in
                lobby.teams[team_id].players]
        return jsonify(200, lobby_players = players_dict)

    @admin_check
    def post(self, lobby_id, team_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        if 'player_id' not in request.form:
            abort(405)
        p_id = request.form['player_id']
        p = Player.query.get(p_id)
        if not p:
            abort(405)
        t.append_player(p)
        db.session.commit()
        return jsonify(201)

class LobbyPlayerAPI(MethodView):
    def get(self, lobby_id, team_id, player_id):
        lobby = Lobby.query.get_or_404(lobby_id)
        if team_id >= len(lobby.teams) or team_id < 0:
            abort(404)
        team = lobby.teams[team_id]
        player = Player.query.get_or_404(player_id)
        if not player in team:
            abort(404)
        return jsonify(200,
                lobby_player = make_lobby_player_dict(team.get_lobby_player(player)))

    @admin_check
    def put(self, lobby_id, team_id, player_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        p = Player.query.get(player_id)
        if not p or p not in t:
            abort(404)
        lp = t.get_lobby_player(p)
        if 'class_id' in request.form:
            lp.class_id = request.form['class_id']
        if 'ready' in request.form:
            lp.ready = request.form['ready']
        db.session.commit()
        return jsonify(200)

    @admin_check
    def delete(self, lobby_id, team_id, player_id):
        l = Lobby.query.get(lobby_id)
        if l is None:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        p = Player.query.get(player_id)
        if not p or p not in t:
            abort(404)
        t.remove_player(p)
        db.session.commit()
        return jsonify(200)
