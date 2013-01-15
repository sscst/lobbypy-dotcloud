from json import dumps
from mock import patch
from flask import g, session
from flask.ext.testing import TestCase
from lobbypy import create_app, config_app
from lobbypy.utils import db
from lobbypy.models import Player, Lobby, Team

class RestTest(TestCase):
    def create_app(self):
        app = create_app()
        config_app(app, SQLALCHEMY_DATABASE_URI='sqlite://', TESTING=True)
        return app

    def setUp(self):
        db.create_all()
        a = Player('')
        a.admin = True
        db.session.add(a)
        db.session.commit()
        self.admin = a
        with self.client.session_transaction() as sess:
            sess['user_id'] = a.id

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_player_listing(self, magic_get_summary):
        db.session.add(Player('0'))
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/players')
        self.assertStatus(resp, 200)
        self.assertTrue('players' in resp.json)
        players = resp.json['players']
        self.assertEqual(len(players), 2)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_player(self, magic_get_summary):
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/players/%d' % self.admin.id)
        self.assertStatus(resp, 200)
        self.assertTrue('player' in resp.json)
        player = resp.json['player']
        self.assertTrue('id' in player)
        self.assertTrue('steam_id' in player)
        self.assertTrue('name' in player)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_lobby_listing(self, magic_get_summary):
        p = Player('0')
        db.session.add(Lobby('A', self.admin, 'a', '', ''))
        db.session.add(Lobby('B', p, 'b', '', ''))
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies')
        self.assertTrue('lobbies' in resp.json)
        lobbies = resp.json['lobbies']
        self.assertEqual(len(lobbies), 2)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_lobby(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d' % l.id)
        self.assertTrue('lobby' in resp.json)
        lobby = resp.json['lobby']
        self.assertTrue('id' in lobby)
        self.assertTrue('owner' in lobby)
        self.assertTrue('game_map' in lobby)
        self.assertTrue('teams' in lobby)
        self.assertTrue('spectators' in lobby)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_spectator_listing(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        p = Player('0')
        l.spectators.append(self.admin)
        l.spectators.append(p)
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d/spectators' % l.id)
        self.assertTrue('spectators' in resp.json)
        specs = resp.json['spectators']
        self.assertEqual(len(specs), 2)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_spectator(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        l.spectators.append(self.admin)
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d/spectators/%d' % (l.id,
            self.admin.id))
        self.assertTrue('spectator' in resp.json)
        spec = resp.json['spectator']
        self.assertTrue('id' in spec)
        self.assertTrue('steam_id' in spec)
        self.assertTrue('name' in spec)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_team_listing(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        l.teams.append(Team('Red'))
        l.teams.append(Team('Blu'))
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d/teams' % l.id)
        self.assertTrue('teams' in resp.json)
        teams = resp.json['teams']
        self.assertEqual(len(teams), 2)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_team(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        l.teams.append(Team('Red'))
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d/teams/0' % l.id)
        self.assertTrue('team' in resp.json)
        team = resp.json['team']
        self.assertTrue('name' in team)
        self.assertTrue('players' in team)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_lobby_player_listing(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        t = Team('Red')
        p = Player('0')
        t.join(self.admin)
        t.join(p)
        l.teams.append(t)
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d/teams/0/players' % l.id)
        self.assertTrue('lobby_players' in resp.json)
        l_players = resp.json['lobby_players']
        self.assertEqual(len(l_players), 2)

    @patch('lobbypy.models.player.get_player_summary_for_steam_id')
    def test_get_lobby_player(self, magic_get_summary):
        l = Lobby('A', self.admin, '', '', '')
        t = Team('Red')
        t.join(self.admin)
        l.teams.append(t)
        db.session.add(l)
        db.session.commit()
        magic_get_summary.return_value = {'personaname':'Anonymous'}
        resp = self.client.get('/admin/rest/lobbies/%d/teams/0/players/%d' %
                (l.id, self.admin.id))
        self.assertTrue('lobby_player' in resp.json)
        player = resp.json['lobby_player']
        self.assertTrue('player' in player)
        self.assertTrue('class_id' in player)
        self.assertTrue('ready' in player)

    def test_create_player(self):
        resp = self.client.post('/admin/rest/players', data=dict(steam_id='0'))
        p = Player.query.filter_by(steam_id = '0').first()
        self.assertStatus(resp, 201)
        self.assertTrue(p)
        self.assertEqual(p.steam_id, '0')

    def test_update_player(self):
        p = Player('0')
        db.session.add(p)
        db.session.commit()
        resp = self.client.put('/admin/rest/players/%d' % p.id,
                data=dict(steam_id='1'))
        self.assertStatus(resp, 200)
        p = db.session.merge(p)
        self.assertEqual(p.steam_id, '1')

    def test_delete_player(self):
        p = Player('0')
        db.session.add(p)
        db.session.commit()
        resp = self.client.delete('/admin/rest/players/%d' % p.id)
        self.assertStatus(resp, 200)
        players = Player.query.filter_by(steam_id = '0').all()
        self.assertEqual(len(players), 0)

    def test_create_lobby(self):
        resp = self.client.post('/admin/rest/lobbies', data=dict(owner_id =
            self.admin.id, name = 'Lobby', server_address = 'x.x.x.x',
            rcon_password = 'xxxx', game_map = 'xxxxx', password = 'xxxx'))
        self.assertStatus(resp, 201)
        l = Lobby.query.first()
        self.assertEqual(l.name, 'Lobby')

    def test_update_lobby(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        resp = self.client.put('/admin/rest/lobbies/%d' % l.id, data=dict(name = 'Test'))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(l.name, 'Test')

    def test_delete_lobby(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d' % l.id)
        lobbies = Lobby.query.all()
        self.assertStatus(resp, 200)
        self.assertEqual(len(lobbies), 0)

    def test_append_team(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        db.session.add(l)
        db.session.commit()
        resp = self.client.post('/admin/rest/lobbies/%d/teams' % l.id,
                data=dict(name='Red'))
        self.assertStatus(resp, 201)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams), 1)
        self.assertEqual(l.teams[0].name, 'Red')

    def test_update_team(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        t = Team('Red')
        l.teams.append(t)
        db.session.add(l)
        db.session.commit()
        resp = self.client.put('/admin/rest/lobbies/%d/teams/0' % l.id,
                data=dict(name='Blu'))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(l.teams[0].name, 'Blu')

    def test_delete_team(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        t = Team('Red')
        l.teams.append(t)
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d/teams/0' % l.id)
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams), 0)

    def test_append_spectator(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        p = Player('0')
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.post('/admin/rest/lobbies/%d/spectators' % l.id,
                data=dict(player_id = p.id))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.spectators), 1)

    def test_remove_spectator(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        p = Player('0')
        l.spectators.append(p)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d/spectators/%d' % (
            l.id, p.id))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.spectators), 0)

    def test_append_lobby_player(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        t = Team('Red')
        p = Player('0')
        l.teams.append(t)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.post('/admin/rest/lobbies/%d/teams/0/players' %
            l.id, data=dict(player_id = p.id))
        self.assertStatus(resp, 201)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams[0].players), 1)

    def test_update_lobby_player(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        t = Team('Red')
        p = Player('0')
        t.join(p)
        l.teams.append(t)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.put('/admin/rest/lobbies/%d/teams/0/players/%d' %
            (l.id, p.id), data=dict(class_id = 0))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams[0].players), 1)
        self.assertEqual(l.teams[0].players[0].class_id, 0)

    def test_delete_lobby_player(self):
        l = Lobby('Lobby', self.admin, 'test', 'test', 'test')
        t = Team('Red')
        p = Player('0')
        t.join(p)
        l.teams.append(t)
        db.session.add(p)
        db.session.add(l)
        db.session.commit()
        resp = self.client.delete('/admin/rest/lobbies/%d/teams/0/players/%d' %
            (l.id, p.id))
        self.assertStatus(resp, 200)
        l = db.session.merge(l)
        self.assertEqual(len(l.teams[0].players), 0)
