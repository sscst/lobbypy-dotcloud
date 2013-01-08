from flask import request, abort
from flask.views import MethodView

from lobbypy.models import Player, Lobby, Team, LobbyPlayer
from lobbypy.utils import db
from .utils import admin_check, jsonify

class PlayerListingAPI(MethodView):
    def get(self):
        pass

    @admin_check
    def post(self):
        p = Player(request.form['steam_id'])
        db.session.add(p)
        db.session.commit()
        return jsonify(201, id=p.id)

class PlayerAPI(MethodView):
    def get(self, player_id):
        pass

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
        pass

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
        pass

    @admin_check
    def put(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if not l:
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
        return jsonify(200)

    @admin_check
    def delete(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if not l:
            abort(404)
        db.session.delete(l)
        db.session.commit()
        return jsonify(200)

class SpectatorListingAPI(MethodView):
    def get(self, lobby_id):
        pass

    @admin_check
    def post(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if not l:
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
        pass

    @admin_check
    def delete(self, lobby_id, player_id):
        l = Lobby.query.get(lobby_id)
        if not l:
            abort(404)
        p = Player.query.get(player_id)
        if not p:
            abort(405)
        l.spectators.remove(p)
        db.session.commit()
        return jsonify(200)

class TeamListingAPI(MethodView):
    def get(self, lobby_id):
        pass

    @admin_check
    def post(self, lobby_id):
        l = Lobby.query.get(lobby_id)
        if not l:
            abort(404)
        if 'name' not in request.form:
            abort(405)
        t = Team(request.form['name'])
        l.teams.append(t)
        db.session.commit()
        return jsonify(201, id=len(l.teams) - 1)

class TeamAPI(MethodView):
    def get(self, lobby_id, team_id):
        pass

    @admin_check
    def put(self, lobby_id, team_id):
        l = Lobby.query.get(lobby_id)
        if not l:
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
        if not l:
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
        pass

    @admin_check
    def post(self, lobby_id, team_id):
        l = Lobby.query.get(lobby_id)
        if not l:
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
        pass

    @admin_check
    def put(self, lobby_id, team_id, player_id):
        l = Lobby.query.get(lobby_id)
        if not l:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        p = Player.query.get(player_id)
        if not p or not t.has_player(p):
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
        if not l:
            abort(404)
        if team_id >= len(l.teams):
            abort(404)
        elif team_id < 0:
            abort(404)
        t = l.teams[team_id]
        p = Player.query.get(player_id)
        if not p or not t.has_player(p):
            abort(404)
        t.remove_player(p)
        db.session.commit()
        return jsonify(200)
