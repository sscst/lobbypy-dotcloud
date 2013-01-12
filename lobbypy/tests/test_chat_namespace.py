from mock import MagicMock, patch
from json import dumps
from flask import current_app, g
from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class ChatNamespaceTest(TestCase):
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
        from lobbypy.namespaces.chat import ChatNamespace
        if environ is None:
            environ = {'socketio': MagicMock()}
        ctx = self.app.test_request_context('/socket.io/1')
        ns = ChatNamespace(environ, ns_name, request=(ctx.app, ctx.request))
        ns.spawn = MagicMock()
        self.ctxs.insert(0, ns.ctx)
        # need to call this as it's called by real virtsocket
        ns.initialize()
        return ns

    def _makeRedisMessage(self, event, *args):
        data = dict()
        data['event'] = event
        data['args'] = args
        return {
                'type': 'message',
                'data': dumps(data),
                }

    def test_on_join(self):
        instance = self._makeOne()
        instance.on_join({'type':'channel', 'dest':'root'})
        self.assertTrue('/chat/channel/root' in instance.pubsub.channels)

    def test_on_part(self):
        instance = self._makeOne()
        instance.pubsub.subscribe('/chat/channel/root')
        instance.on_part({'type':'channel', 'dest':'root'})
        self.assertTrue('/chat/channel/root' not in instance.pubsub.channels)

    @patch('lobbypy.namespaces.chat.ChatNamespace.broadcast_event')
    def test_on_send(self, magic_broadcast):
        from lobbypy.models import Player
        player = Player('0')
        db.session.add(player)
        db.session.commit()
        instance = self._makeOne()
        g.player = player
        instance.pubsub.subscribe('/chat/channel/root')
        rv = instance.on_send({'type':'channel', 'dest':'root'}, 'test')
        magic_broadcast.assert_called_once_with('/chat/channel/root', 'send',
                {'type':'channel', 'dest':'root'}, player.id, 'test')
