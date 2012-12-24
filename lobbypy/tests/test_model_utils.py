from mock import MagicMock
from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db

class ModelUtilsTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _make_team(self, id=0, name='Red',
            lobby_player=None):
        t = MagicMock()
        t.id = id
        t.name = name
        lobby_player = lobby_player or self._make_lobby_player()
        t.players = [lobby_player]
        return t

    def _make_lobby_player(self, class_id=0, ready=True, player=None):
        lp = MagicMock()
        lp.class_id = class_id
        lp.ready = ready
        lp.player = player or self._make_player()
        return lp

    def _make_player(self, id=0, steam_id='0', name='Name'):
        p = MagicMock()
        p.id = id
        p.steam_id = steam_id
        p.name = name
        return p

    def test_make_lobby_item_dict(self):
        l = MagicMock()
        l.owner = self._make_player()
        l.id = 0
        l.name = 'Lobby'
        l.game_map = 'cp_badlands'
        l.player_count = 18
        l.spectator_count = 9
        l_info = {
                'id': 0,
                'owner': {
                    'id': 0,
                    'name': 'Name',
                    'steam_id': '0',
                    },
                'name': 'Lobby',
                'game_map': 'cp_badlands',
                'player_count': 18,
                'spectator_count': 9,
                }
        from lobbypy.models.utils import make_lobby_item_dict
        rv = make_lobby_item_dict(l)
        self.assertEqual(rv, l_info)

    def test_make_lobby_dict(self):
        l = MagicMock()
        l.owner = self._make_player()
        l.id = 0
        l.name = 'Lobby'
        l.game_map = 'cp_badlands'
        l.teams = [self._make_team()]
        l.spectators = [self._make_player()]
        p_dict = {
                    'id': 0,
                    'name': 'Name',
                    'steam_id': '0',
                    }
        l_info = {
                'id': 0,
                'owner': p_dict,
                'name': 'Lobby',
                'game_map': 'cp_badlands',
                'spectators': [p_dict],
                'teams': [{
                    'id': 0,
                    'name': 'Red',
                    'players': [{
                        'class_id': 0,
                        'ready': True,
                        'player': p_dict,
                        }]
                    }],
                }
        from lobbypy.models.utils import make_lobby_dict
        rv = make_lobby_dict(l)
        self.assertEqual(rv, l_info)

    def test_make_team_dict(self):
        t = MagicMock()
        t.name = 'Red'
        t.players = [self._make_lobby_player()]
        p_dict = {
                    'id': 0,
                    'name': 'Name',
                    'steam_id': '0',
                    }
        t_info = {
                'id': 0,
                'name': 'Red',
                    'players': [{
                        'class_id': 0,
                        'ready': True,
                        'player': p_dict,
                    }]
                }
        from lobbypy.models.utils import make_team_dict
        rv = make_team_dict(0, t)
        self.assertEqual(rv, t_info)

    def test_make_lobby_player_dict(self):
        lp = MagicMock()
        lp.class_id = 0
        lp.ready = True
        lp.player = MagicMock()
        lp.player.id = 0
        lp.player.name = 'Name'
        lp.player.steam_id = '0'
        lp_info = {
                'class_id': 0,
                'ready': True,
                'player': {
                    'id': 0,
                    'name': 'Name',
                    'steam_id': '0',
                    },
                }
        from lobbypy.models.utils import make_lobby_player_dict
        rv = make_lobby_player_dict(lp)
        self.assertEqual(rv, lp_info)

    def test_make_player_dict(self):
        p = MagicMock()
        p.id = 0
        p.steam_id = '0'
        p.name = 'Name'
        p_info = {
                'id': 0,
                'steam_id': '0',
                'name': 'Name',
                }
        from lobbypy.models.utils import make_player_dict
        rv = make_player_dict(p)
        self.assertEqual(rv, p_info)
