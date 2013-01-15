from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class TeamModelTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _makeOne(self, name='Red'):
        from lobbypy.models import Team
        return Team(name)

    def test_len(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        self.assertEqual(len(instance), 1)

    def test_contains(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        self.assertTrue(p in instance)

    def test_not_contains(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        p = Player('0')
        self.assertTrue(not p in instance)

    def test_get_lobby_player(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        lp = instance.get_lobby_player(p)
        self.assertEqual(lp.player, p)

    def test_not_get_lobby_player(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        p = Player('0')
        self.assertRaises(IndexError, instance.get_lobby_player, p)

    def test_append(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.append(lp)
        self.assertEqual(len(instance.players), 1)
        self.assertEqual(instance.players[0], lp)

    def test_join(self):
        instance = self._makeOne()
        from lobbypy.models import Player
        p = Player('0')
        instance.join(p)
        self.assertEqual(len(instance.players), 1)
        self.assertEqual(instance.players[0].player, p)

    def test_pop(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        rv = instance._pop(p)
        self.assertEqual(rv, lp)
        self.assertEqual(len(instance.players), 0)

    def test_leave(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        instance.leave(p)
        self.assertEqual(len(instance.players), 0)

    def test_set_class(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        instance.set_class(p, 1)
        self.assertEqual(instance.players[0].class_id, 1)

    def test_toggle_ready(self):
        instance = self._makeOne()
        from lobbypy.models import Player, LobbyPlayer
        p = Player('0')
        lp = LobbyPlayer(p)
        instance.players.append(lp)
        instance.toggle_ready(p)
        self.assertTrue(instance.players[0].ready)
