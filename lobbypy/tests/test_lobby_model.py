from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class LobbyModelTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _makeOne(self, owner=None, name='Lobby', server_address='server:9999',
            game_map='cp_lololol', password='password'):
        from lobbypy.models import Lobby
        if owner is None:
            from lobbypy.models import Player
            owner = Player('-1')
        return Lobby(name, owner, server_address, game_map, password)

    def test_player_count(self):
        instance = self._makeOne()
        from lobbypy.models import Player, Team, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        t_A = Team('Red')
        t_A.players.extend(2 * [lp])
        t_B = Team('Blu')
        t_A.players.extend(3 * [lp])
        instance.teams.extend([t_A, t_B])
        self.assertEqual(instance.player_count, 5)

    def test_spectator_count(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        p = Player('0')
        instance.spectators.extend(2 * [p])
        self.assertEqual(instance.spectator_count, 2)

    def test_join(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        p = Player('0')
        instance.join(p)
        self.assertEqual(len(instance.spectators), 1)
        self.assertEqual(instance.spectators[0], p)

    def test_leave(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        p = Player('0')
        instance.spectators.append(p)
        instance.leave(p)
        self.assertEqual(len(instance.spectators), 0)

    def test_set_team(self):
        instance = self._makeOne()
        from lobbypy.models import Player, Team
        t = Team('Red')
        instance.teams.append(t)
        p = Player('0')
        instance.spectators.append(p)
        instance.set_team(p, 0)
        self.assertEqual(len(instance.teams[0].players), 1)
        self.assertEqual(instance.teams[0].players[0].player, p)

    def test_set_class(self):
        instance = self._makeOne()
        from lobbypy.models import Player, Team, LobbyPlayer
        t = Team('Red')
        p = Player('0')
        lp = LobbyPlayer(p)
        t.players.append(lp)
        instance.teams.append(t)
        instance.set_class(p, 0)
        self.assertEqual(instance.teams[0].players[0].class_id, 0)

    def test_toggle_ready(self):
        instance = self._makeOne()
        from lobbypy.models import Player, Team, LobbyPlayer
        t = Team('Red')
        p = Player('0')
        lp = LobbyPlayer(p)
        t.players.append(lp)
        instance.teams.append(t)
        instance.toggle_ready(p)
        self.assertTrue(instance.teams[0].players[0].ready)
