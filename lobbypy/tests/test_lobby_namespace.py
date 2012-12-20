from mock import MagicMock, patch
from flask import g
from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from mock import patch, MagicMock
from lobbypy.utils import db
from lobbypy.models import Player, Lobby, Team

class LobbyNamespaceTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()
        self.ctxs = []

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        [ctx.pop() for ctx in self.ctxs]

    def _makeOne(self, environ=None, ns_name='lobby'):
        from lobbypy.namespaces.lobby import LobbyNamespace
        if environ is None:
            environ = {'socketio': MagicMock()}
        ctx = self.app.test_request_context('/socket.io/1')
        ns = LobbyNamespace(environ, ns_name, request=ctx.request)
        self.ctxs.insert(0, ns.ctx)
        # need to call this as it's called by real virtsocket
        ns.initialize()
        ns.spawn = MagicMock()
        return ns

    def _makeRedisMessage(self, data_type, **data):
        data['type'] = data_type
        return {
                'type': 'message',
                'data': dumps(data),
                }

    def test_initial_acl(self):
        instance = self._makeOne()
        rv = instance.get_initial_acl()
        self.assertEqual(rv, set(['on_join', 'recv_connect']))

    def test_on_create_lobby(self):
        instance = self._makeOne()
        p = Player('0')
        g.player = p
        instance.recv_connect()
        rvs = instance.on_create_lobby('test', 'test', 'test')
        lobby = Lobby.query.first()
        self.assertTrue(rvs[0])
        self.assertEqual(rvs[1], lobby.id)

    def test_on_join(self):
        instance = self._makeOne()
        o = Player('')
        l = Lobby('', o, '', '', '')
        db.session.add(o)
        db.session.add(l)
        db.session.commit()
        p = Player('0')
        instance.ctx.g.player = p
        instance.recv_connect()
        instance.spawn.return_value = 'jerb'
        rv = instance.on_join(l.id)
        self.assertTrue(rv)
        l = Lobby.query.first()
        self.assertEqual(l.spectators[0], p)
        self.assertEqual(instance.allowed_methods, set(['on_leave',
            'recv_connect', 'on_set_team']))
        self.assertEqual(instance.listener_job, 'jerb')
        self.assertEqual(instance.lobby_id, l.id)

    def test_on_leave(self):
        instance = self._makeOne()
        o = Player('')
        l = Lobby('', o, '', '', '')
        p = Player('0')
        l.join(p)
        db.session.add(o)
        db.session.add(l)
        db.session.add(p)
        db.session.commit()
        instance.lobby_id = l.id
        instance.ctx.g.player = p
        instance.allowed_methods = set(['on_leave',
            'recv_connect', 'on_set_team'])
        instance.listener_job = MagicMock()
        instance.on_leave()
        self.assertEqual(instance.allowed_methods,
                set(['on_join', 'on_create_lobby', 'recv_connect']))
        self.assertTrue(instance.lobby_id is None)
        self.assertEqual(len(l.spectators), 0)
        instance.listener_job.kill.assert_called_once()

    def test_on_set_team(self):
        instance = self._makeOne()
        o = Player('')
        l = Lobby('', o, '', '', '')
        t = Team('Red')
        l.teams.append(t)
        p = Player('0')
        l.join(p)
        db.session.add(o)
        db.session.add(l)
        db.session.add(t)
        db.session.add(p)
        db.session.commit()
        instance.lobby_id = l.id
        instance.ctx.g.player = p
        instance.allowed_methods = set(['on_leave',
            'recv_connect', 'on_set_team'])
        instance.on_set_team(0)
        self.assertEqual(instance.allowed_methods, set(['on_leave',
            'recv_connect', 'on_set_class', 'on_toggle_ready', 'on_set_team']))
        self.assertEqual(l.teams[0].players[0].player, p)

    def test_on_set_class(self):
        instance = self._makeOne()
        o = Player('')
        l = Lobby('', o, '', '', '')
        t = Team('Red')
        l.teams.append(t)
        p = Player('0')
        t.append_player(p)
        db.session.add(o)
        db.session.add(l)
        db.session.add(t)
        db.session.add(p)
        db.session.commit()
        instance.lobby_id = l.id
        instance.ctx.g.player = p
        instance.allowed_methods = set(['on_leave',
            'recv_connect', 'on_set_team', 'on_set_class', 'on_toggle_ready'])
        instance.on_set_class(0)
        self.assertEqual(instance.allowed_methods, set(['on_leave',
            'recv_connect', 'on_set_class', 'on_toggle_ready', 'on_set_team']))
        self.assertEqual(l.teams[0].players[0].class_id, 0)

    def test_on_toggle_ready(self):
        instance = self._makeOne()
        o = Player('')
        l = Lobby('', o, '', '', '')
        t = Team('Red')
        l.teams.append(t)
        p = Player('0')
        t.append_player(p)
        db.session.add(o)
        db.session.add(l)
        db.session.add(t)
        db.session.add(p)
        db.session.commit()
        instance.lobby_id = l.id
        instance.ctx.g.player = p
        instance.allowed_methods = set(['on_leave',
            'recv_connect', 'on_set_team', 'on_set_class', 'on_toggle_ready'])
        instance.on_toggle_ready()
        self.assertEqual(instance.allowed_methods, set(['on_leave',
            'recv_connect', 'on_toggle_ready']))
        self.assertTrue(l.teams[0].players[0].ready)

    def test_on_start(self):
        pass
