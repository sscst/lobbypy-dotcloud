from mock import MagicMock, patch
from json import dumps
from flask import current_app
from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class LobbiesNamespaceTest(TestCase):
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

    def _makeOne(self, environ=None, ns_name='lobbies'):
        from lobbypy.namespaces.lobbies import LobbiesNamespace
        if environ is None:
            environ = {'socketio': MagicMock()}
        ctx = self.app.test_request_context('/socket.io/1')
        ns = LobbiesNamespace(environ, ns_name, request=ctx.request)
        self.ctxs.insert(0, ns.ctx)
        # need to call this as it's called by real virtsocket
        ns.initialize()
        ns.spawn = MagicMock()
        return LobbiesNamespace(environ, ns_name)

    def _makeRedisMessage(self, event, *args):
        data = dict()
        data['event'] = event
        data['args'] = args
        return {
                'type': 'message',
                'data': dumps(data),
                }

    @patch('lobbypy.namespaces.lobbies.LobbiesNamespace.emit')
    @patch('lobbypy.namespaces.base.redis')
    def test_listen_update_message(self, magic_module, magic_method):
        lobby_json = {'name':'Lobby'}
        redis = magic_module.StrictRedis.return_value
        pubsub = redis.pubsub.return_value

        pubsub.listen.return_value = [
                self._makeRedisMessage('update', lobby_json)]
        instance = self._makeOne()
        instance.listener('/lobby/')
        magic_method.assert_called_once_with('update', lobby_json)

    @patch('lobbypy.namespaces.lobbies.LobbiesNamespace.emit')
    @patch('lobbypy.namespaces.base.redis')
    def test_listen_create_message(self, magic_module, magic_method):
        lobby_json = {'name':'Lobby'}
        redis = magic_module.StrictRedis.return_value
        pubsub = redis.pubsub.return_value

        pubsub.listen.return_value = [
                self._makeRedisMessage('create', lobby_json)]
        instance = self._makeOne()
        instance.listener('/lobby/')
        magic_method.assert_called_once_with('create', lobby_json)

    @patch('lobbypy.namespaces.lobbies.LobbiesNamespace.emit')
    @patch('lobbypy.namespaces.base.redis')
    def test_listen_destroy_message(self, magic_module, magic_method):
        redis = magic_module.StrictRedis.return_value
        pubsub = redis.pubsub.return_value

        pubsub.listen.return_value = [
                self._makeRedisMessage('delete', 1)]
        instance = self._makeOne()
        instance.listener('/lobby/')
        magic_method.assert_called_once_with('delete', 1)

    @patch('lobbypy.namespaces.lobbies.Lobby')
    @patch('lobbypy.namespaces.lobbies.make_lobby_item_dict')
    @patch('lobbypy.namespaces.lobbies.LobbiesNamespace.emit')
    def test_on_get_lobby_listing(self, magic_emit,
            magic_make_lobby_dict, magic_Lobby):
        from lobbypy.models import Lobby, Player
        p = Player('0')
        lobbies = [
                Lobby('A', p, '', '', ''),
                Lobby('B', p, '', '', ''),
                ]
        magic_Lobby.query.all.return_value = lobbies
        lobbies_dict = [
                {'name': 'A'},
                {'name': 'B'},
                ]
        json_rvs = list(lobbies_dict)
        def side_effect(*args, **kwargs):
            return json_rvs.pop(0)
        magic_make_lobby_dict.side_effect = side_effect
        instance = self._makeOne()
        rvs = instance.on_get_lobby_listing()
        self.assertTrue(rvs[0])
        self.assertEqual(rvs[1], lobbies_dict)
