from flask.ext.testing import TestCase
from lobbypy import create_app, db

class LobbyModelTest(TestCase):
    def create_app(self):
        return create_app(SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _makeOne(self, owner=None, name='Lobby', server='pass@server:9999',
            game_map='cp_lololol', password='password'):
        from lobbypy.models import Lobby
        if owner is None:
            from lobbypy.models import Player
            owner = Player('-1')
        return Lobby(name, owner, server, game_map, password)

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
