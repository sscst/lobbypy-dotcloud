from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class ControllersTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _callFUT(self, player):
        from lobbypy.controllers import leave_or_delete_all_lobbies
        return leave_or_delete_all_lobbies(player)

    def test_with_no_lobbies(self):
        from lobbypy.models import Player
        p = Player('0')
        db.session.add(p)
        db.session.commit()
        rv = self._callFUT(p)
        l_dels = []
        for l_del in rv:
            l_dels.append(l_del)
        self.assertEqual(len(l_dels), 0)

    def test_with_owned_lobbies(self):
        from lobbypy.models import Player, Lobby
        p = Player('0')
        db.session.add(p)
        l = Lobby('test', p, 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        rv = self._callFUT(p)
        l_dels = []
        for l_del in rv:
            l_dels.append(l_del)
        self.assertEqual(len(l_dels), 1)
        self.assertEqual(l_dels[0], (l, True))

    def test_with_speced_lobbies(self):
        from lobbypy.models import Player, Lobby
        o = Player('1')
        p = Player('0')
        db.session.add(o)
        db.session.add(p)
        l = Lobby('test', o, 'test', 'test', 'test')
        l.spectators.append(p)
        db.session.add(l)
        db.session.commit()
        rv = self._callFUT(p)
        l_dels = []
        for l_del in rv:
            l_dels.append(l_del)
        self.assertEqual(len(l_dels), 1)
        self.assertEqual(l_dels[0], (l, False))

    def test_with_teamed_lobbies(self):
        from lobbypy.models import Player, Lobby, Team
        o = Player('1')
        p = Player('0')
        db.session.add(o)
        db.session.add(p)
        l = Lobby('test', o, 'test', 'test', 'test')
        t = Team('Red')
        l.teams.append(t)
        l.teams[0].join(p)
        db.session.add(l)
        db.session.commit()
        rv = self._callFUT(p)
        l_dels = []
        for l_del in rv:
            l_dels.append(l_del)
        self.assertEqual(len(l_dels), 1)
        self.assertEqual(l_dels[0], (l, False))
